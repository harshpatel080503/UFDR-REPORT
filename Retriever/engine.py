import os
import time
import re
import numpy as np
import faiss
import sqlite3
from sentence_transformers import SentenceTransformer

from retriever_config import (
    FAISS_DIR,
    PAGEINDEX_DB,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
    RETRIEVER_K,
    SEARCH_DEVICE,
)

try:
    from Reranker.rerank_engine import RerankEngine
    from Reranker.reranker_config import TOP_K_INITIAL, RERANK_DEPTH, TOP_K_FINAL
    RERANKER_AVAILABLE = True
except ImportError:
    RERANKER_AVAILABLE = False

class RetrieverEngine:
    def __init__(self):
        print(f"  Loading Retriever model ({EMBEDDING_MODEL}) ...")
        self.model = SentenceTransformer(EMBEDDING_MODEL, device=SEARCH_DEVICE)
        
        self.indexes = {}
        self.id_maps = {}
        self._load_indexes()
        
        print(f"  Connecting to SQLite PageIndex ({os.path.basename(PAGEINDEX_DB)}) ...")
        self.conn = sqlite3.connect(PAGEINDEX_DB, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        self.reranker = None
        if RERANKER_AVAILABLE:
            self.reranker = RerankEngine()

    def _load_indexes(self):
        """Discover and load all FAISS shards from the indexing output."""
        if not os.path.isdir(FAISS_DIR):
            print(f"FAISS directory not found: {FAISS_DIR}")
            return

        idx_files = [f for f in os.listdir(FAISS_DIR) if f.endswith(".index")]
        if not idx_files:
            print("No FAISS indexes found.")
            return

        print(f"Loading {len(idx_files)} FAISS shards into memory ...")
        for f in sorted(idx_files):
            name = f.replace(".index", "")
            idx_path = os.path.join(FAISS_DIR, f)
            ids_path = os.path.join(FAISS_DIR, f"{name}_ids.npy")
            
            if os.path.exists(ids_path):
                t0 = time.time()
                self.indexes[name] = faiss.read_index(idx_path)
                self.id_maps[name] = np.load(ids_path, allow_pickle=True)
                print(f"    [+] {name:<15} | {len(self.id_maps[name]):>10,} vectors | {time.time()-t0:.2f}s")
            else:
                print(f"    [!] Skipping {name} (missing ID map)")

    def _extract_metadata(self, query: str):
        """Extract User IDs and Dates from the query string."""
        user_match = re.search(r'[A-Z]{3}\d{4}', query)
        user = user_match.group(0) if user_match else None
        
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', query)
        date = date_match.group(0) if date_match else None
        
        return user, date

    def search(self, query: str, k: int = RETRIEVER_K, use_reranker: bool = False):
        """
        End-to-end search: String -> Metadata + Embedding -> FAISS + SQL -> Records
        """
        t0 = time.time()
        faiss_k = TOP_K_INITIAL if (use_reranker and self.reranker) else k

        # 1. Metadata Extraction
        user, date = self._extract_metadata(query)
        
        # 2. Embedding
        query_vec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        query_vec = query_vec.astype(np.float32)

        all_results = []
        
        # 3. Hybrid Search: SQL Metadata Match (Highest priority)
        if user or date:
            sql_pids = self._search_sql_metadata(user, date, k=5)
            for pid in sql_pids:
                all_results.append({
                    "page_id": pid,
                    "distance": 0.0, # Perfect score for metadata match
                    "shard": "sql_metadata"
                })

        # 4. FAISS Semantic Search
        for name, index in self.indexes.items():
            # Optimization: Shard filtering based on date
            if date and name.startswith("http_") and date[:7] not in name:
                continue
                
            distances, indices = index.search(query_vec, faiss_k)
            
            for dist, idx in zip(distances[0], indices[0]):
                if idx >= 0:
                    pid = self.id_maps[name][idx]
                    all_results.append({
                        "page_id": pid,
                        "distance": float(dist),
                        "shard": name
                    })

        # Deduplicate and Sort
        seen_pids = set()
        unique_results = []
        for res in sorted(all_results, key=lambda x: x["distance"]):
            if res["page_id"] not in seen_pids:
                unique_results.append(res)
                seen_pids.add(res["page_id"])
        
        top_candidates = unique_results[:faiss_k]

        # 5. Fetch Records from SQL
        final_records = []
        if top_candidates:
            pids = [r["page_id"] for r in top_candidates]
            records_map = self._fetch_records(pids)
            
            for res in top_candidates:
                rec = records_map.get(res["page_id"])
                if rec:
                    rec_dict = dict(rec)
                    rec_dict["_search_score"] = res["distance"]
                    rec_dict["_shard"] = res["shard"]
                    final_records.append(rec_dict)

        # 6. Reranking
        rerank_dt = 0
        if use_reranker and self.reranker and final_records:
            to_rerank = final_records[:RERANK_DEPTH]
            others    = final_records[RERANK_DEPTH:]
            
            reranked, rerank_dt = self.reranker.rerank(query, to_rerank)
            final_records = reranked + others
            
            final_records = final_records[:TOP_K_FINAL]
        else:
            final_records = final_records[:k]

        elapsed = time.time() - t0
        return final_records, elapsed, rerank_dt

    def _search_sql_metadata(self, user: str, date: str, k: int = 5):
        """Direct SQL search for metadata filters."""
        pids = []
        try:
            cursor = self.conn.cursor()
            if user and date:
                cursor.execute("SELECT page_id FROM documents WHERE user = ? AND date = ? LIMIT ?", (user, date, k))
            elif user:
                cursor.execute("SELECT page_id FROM documents WHERE user = ? LIMIT ?", (user, k))
            elif date:
                cursor.execute("SELECT page_id FROM documents WHERE date = ? LIMIT ?", (date, k))
            else:
                return []
            
            pids = [r["page_id"] for r in cursor.fetchall()]
        except Exception as e:
            print(f"  [!] SQL Metadata Search Error: {e}")
        return pids

    def _fetch_records(self, pids: list):
        if not pids: return {}
        placeholders = ",".join("?" for _ in pids)
        query = f"SELECT * FROM documents WHERE page_id IN ({placeholders})"
        cursor = self.conn.cursor()
        cursor.execute(query, pids)
        rows = cursor.fetchall()
        return {row["page_id"]: row for row in rows}

    def close(self):
        self.conn.close()



