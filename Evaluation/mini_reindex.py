import os
import json
import sqlite3
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Load paths from config
import sys
BASE_DIR = r"E:\Data Science Study\Deep Learning Project\UFDR"
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "Indexing")) # Add this to fix the ModuleNotFoundError

from Indexing.config import EMBEDDING_MODEL, PAGEINDEX_DB

def main():
    GOLDEN_DATASET_PATH = os.path.join(BASE_DIR, "Evaluation", "golden_dataset.json")
    MINI_INDEX_PATH = os.path.join(BASE_DIR, "Evaluation", "mini_eval.index")
    MINI_IDS_PATH = os.path.join(BASE_DIR, "Evaluation", "mini_eval_ids.npy")

    print(f"[*] Loading Golden Dataset...")
    with open(GOLDEN_DATASET_PATH, "r") as f:
        golden_data = json.load(f)

    # Collect all required IDs
    required_ids = set()
    for item in golden_data:
        for eid in item.get("expected_log_ids", []):
            required_ids.add(str(eid))

    print(f"[*] Found {len(required_ids)} unique documents required for evaluation.")

    # Fetch from DB
    print(f"[*] Fetching text from database...")
    conn = sqlite3.connect(PAGEINDEX_DB)
    cursor = conn.cursor()
    
    docs = []
    found_ids = []
    for pid in tqdm(list(required_ids)):
        cursor.execute("SELECT text FROM documents WHERE page_id = ?", (pid,))
        row = cursor.fetchone()
        if row:
            docs.append(row[0])
            found_ids.append(pid)
    conn.close()

    if not docs:
        print("[!] No documents found in database.")
        return

    # Embed using NEW model
    print(f"[*] Loading FINE-TUNED model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    print(f"[*] Embedding {len(docs)} documents (This will be fast)...")
    embeddings = model.encode(docs, show_progress_bar=True, normalize_embeddings=True)

    # Build Mini FAISS Index
    print(f"[*] Building Mini FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(np.array(embeddings).astype('float32'))

    # Save Index and ID mapping
    faiss.write_index(index, MINI_INDEX_PATH)
    np.save(MINI_IDS_PATH, np.array(found_ids, dtype=object))

    print(f"\n[SUCCESS] Mini-Reindex Complete!")
    print(f" - Index saved to: {MINI_INDEX_PATH}")
    print(f" - ID Mapping saved to: {MINI_IDS_PATH}")

if __name__ == "__main__":
    main()
