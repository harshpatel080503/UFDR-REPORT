import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    INPUT_DIR,
    OUTPUT_DIR,
    NON_HTTP_FILES,
    HTTP_FILE,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
    FAISS_NLIST,
    FAISS_M_PQ,
    FAISS_NBITS,
    EMBEDDINGS_DIR,
    PAGEINDEX_DB,
)

def phase_pageindex(allowed_pids: set | None = None, resume: bool = False):
    from page_index import PageIndexBuilder

    builder = PageIndexBuilder(allowed_pids=allowed_pids)
    total   = 0

    existing_sources = {}
    if resume:
        existing_sources = builder.get_source_counts()
        if existing_sources:
            print(f"  Resuming: {len(existing_sources)} sources already in DB.")

    # non-HTTP
    for fname in NON_HTTP_FILES:
        source = fname.replace(".jsonl", "")
        if resume and source in existing_sources:
            print(f"    Skipping {source} (already has {existing_sources[source]:,} rows)")
            continue

        fpath = os.path.join(INPUT_DIR, fname)
        if os.path.exists(fpath):
            total += builder.process_file(fpath, source)
        else:
            print(f"{fname} not found — skipping")

    # HTTP
    source = "http"
    if resume and source in existing_sources:
        # For HTTP, we always try to run it because it's often interrupted,
        # but the user might want to skip if it's already there.
        # Given the request "done till HTTP", they probably want to run HTTP.
        # But if it has millions of rows, maybe it's done.
        # We'll print a warning and proceed with INSERT OR IGNORE.
        print(f"    Notice: {source} already has {existing_sources[source]:,} rows. Re-scanning for missing records...")
    
    fpath = os.path.join(INPUT_DIR, HTTP_FILE)
    if os.path.exists(fpath):
        total += builder.process_file(fpath, source)
    else:
        print(f"{HTTP_FILE} not found — skipping")

    builder.build_sql_indexes()
    builder.print_stats()
    builder.close()

    print(f"\n  Phase 1 ingestion complete. New rows added: {total:,}")
    return total

def phase_embed():
    from embedding_engine import EmbeddingEngine

    engine = EmbeddingEngine()

    print(f"\n{'=' * 60}")
    print("  Phase 2a — Non-HTTP Embeddings")
    print(f"{'=' * 60}")
    n1 = engine.process_non_http()

    print(f"\n{'=' * 60}")
    print("  Phase 2b — HTTP Embeddings  (monthly sharding)")
    print(f"{'=' * 60}")
    n2 = engine.process_http(start_total=n1)

    print(f"\n  Phase 2 total vectors: {n1 + n2:,}")
    engine.close()
    return n1 + n2


def phase_faiss():
    """Build FAISS indexes from saved embedding chunks."""
    from faiss_builder import FAISSBuilder

    builder = FAISSBuilder()
    builder.build_all()


def phase_sync():
    """Trim SQLite database to match generated embeddings."""
    import sqlite3
    import glob
    import numpy as np

    print(f"\n{'#' * 60}")
    print("  PHASE 2.5 — Synchronizing Database")
    print(f"{'#' * 60}")

    if not os.path.exists(PAGEINDEX_DB):
        print("  PageIndex DB not found. Skipping sync.")
        return

    # 1. Collect all page_ids from chunks
    print("  Collecting page_ids from embedding chunks...")
    all_pids = set()
    chunks = glob.glob(os.path.join(EMBEDDINGS_DIR, "**", "chunk_*.npz"), recursive=True)
    if not chunks:
        print("  No embedding chunks found. Skipping sync.")
        return

    for p in chunks:
        try:
            with np.load(p, allow_pickle=True) as d:
                pids = d["page_ids"]
                all_pids.update(pids.tolist())
        except Exception as e:
            print(f"    Error reading {p}: {e}")

    print(f"  Found {len(all_pids):,} unique page_ids with embeddings.")

    # 2. Sync SQLite
    conn = sqlite3.connect(PAGEINDEX_DB)
    cursor = conn.cursor()

    # Create temporary table for filtering to speed up DELETE
    cursor.execute("CREATE TEMPORARY TABLE valid_pids (page_id TEXT PRIMARY KEY)")
    cursor.executemany("INSERT INTO valid_pids VALUES (?)", [(pid,) for pid in all_pids])
    conn.commit()

    tables = ["documents"]
    for tbl in tables:
        print(f"    Trimming {tbl} ...")
        cursor.execute(f"DELETE FROM {tbl} WHERE page_id NOT IN (SELECT page_id FROM valid_pids)")
        conn.commit()

    print("  Vacuuming database to reclaim space...")
    cursor.execute("VACUUM")
    conn.commit()
    conn.close()
    print("  Synchronization complete.")


def load_allowed_pids():
    """Scan all embedding chunks to get the set of page_ids we actually have."""
    import glob
    import numpy as np
    print("\n  Pre-scanning embedding chunks for allowed page_ids...")
    all_pids = set()
    chunks = glob.glob(os.path.join(EMBEDDINGS_DIR, "**", "chunk_*.npz"), recursive=True)
    if not chunks:
        print("  [!] No embedding chunks found. Phase 1 will ingest NOTHING.")
        return set()

    for p in chunks:
        try:
            with np.load(p, allow_pickle=True) as d:
                all_pids.update(d["page_ids"].tolist())
        except:
            pass
    print(f"  Loaded {len(all_pids):,} allowed page_ids.")
    return all_pids


def save_metadata():
    meta = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dim": EMBEDDING_DIM,
        "faiss_params": {
            "nlist": FAISS_NLIST,
            "m_pq": FAISS_M_PQ,
            "nbits": FAISS_NBITS,
        },
        "indexes": {},
    }

    faiss_dir = os.path.join(OUTPUT_DIR, "faiss")
    if os.path.isdir(faiss_dir):
        for f in sorted(os.listdir(faiss_dir)):
            if f.endswith(".index"):
                name = f.replace(".index", "")
                size = os.path.getsize(os.path.join(faiss_dir, f))
                meta["indexes"][name] = {
                    "file": f,
                    "size_mb": round(size / (1024 ** 2), 2),
                }

    db_path = os.path.join(OUTPUT_DIR, "page_index.db")
    if os.path.exists(db_path):
        meta["page_index_db_mb"] = round(
            os.path.getsize(db_path) / (1024 ** 2), 2
        )

    out = os.path.join(OUTPUT_DIR, "index_metadata.json")
    with open(out, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"\n  Metadata saved → {out}")

BANNER = r"""
    +-------------------------------------------------------+
    |        UFDR Copilot -- Indexing Pipeline              |
    +-------------------------------------------------------+
    |  Phase 1  |  Filtered Ingestion (Only embedded docs) |
    |  Phase 2  |  Embeddings  (sentence-transformers)      |
    |  Phase 3  |  FAISS       (IVF + PQ sharded)           |
    +-------------------------------------------------------+
"""


def main():
    parser = argparse.ArgumentParser(
        description="UFDR Copilot — Indexing Pipeline",
    )
    parser.add_argument(
        "--phase",
        choices=["pageindex", "embed", "faiss", "all"],
        default="all",
        help="Which phase to run  (default: all)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume Phase 1 without deleting existing database",
    )
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(BANNER)

    t0 = time.time()

    if args.phase in ("pageindex", "all"):
        print(f"\n{'#' * 60}")
        print("  PHASE 1 — Filtered PageIndex")
        print(f"{'#' * 60}")
        
        if os.path.exists(PAGEINDEX_DB):
            if args.resume:
                print(f"  [RESUME] Keeping existing database: {os.path.basename(PAGEINDEX_DB)}")
            else:
                print(f"  Removing old inconsistent database: {os.path.basename(PAGEINDEX_DB)}")
                os.remove(PAGEINDEX_DB)
                # Remove WAL files if they exist
                for ext in ["-wal", "-shm"]:
                    if os.path.exists(PAGEINDEX_DB + ext):
                        os.remove(PAGEINDEX_DB + ext)

        allowed = load_allowed_pids()
        phase_pageindex(allowed_pids=allowed, resume=args.resume)

    if args.phase in ("embed", "all"):
        print(f"\n{'#' * 60}")
        print("  PHASE 2 — Embeddings")
        print(f"{'#' * 60}")
        phase_embed()

    if args.phase in ("faiss", "all"):
        print(f"\n{'#' * 60}")
        print("  PHASE 3 — FAISS Indexes")
        print(f"{'#' * 60}")
        phase_faiss()

    save_metadata()

    elapsed = time.time() - t0
    hours, rem = divmod(int(elapsed), 3600)
    mins, secs = divmod(rem, 60)

    print(f"\n{'=' * 60}")
    print(f"  [OK]  Pipeline complete in {hours}h {mins}m {secs}s")
    print(f"{'=' * 60}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print()


if __name__ == "__main__":
    main()
