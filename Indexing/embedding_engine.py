import os
import json
import time
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

# Limit internal threading per worker to prevent CPU over-subscription
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
torch.set_num_threads(1)

try:
    import orjson
    def _parse(line: str):
        return orjson.loads(line)
except ImportError:
    def _parse(line: str):
        return json.loads(line)

from config import (
    INPUT_DIR,
    EMBEDDINGS_DIR,
    EMBEDDING_MODEL,
    ENCODE_BATCH_SIZE,
    CHUNK_SIZE,
    NON_HTTP_FILES,
    HTTP_FILE,
    HTTP_MONTHS,
    INDEXING_LIMIT,
)


class EmbeddingEngine:

    def __init__(self):
        print("\n  Loading embedding model")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model  = SentenceTransformer(EMBEDDING_MODEL, device=self.device)
        
        # SPEED-RUN OPTIMIZATION: Limit sequence length to 64
        # This makes the neural network math significantly faster
        self.model.max_seq_length = 64
        
        print(f"Model loaded on {self.device.upper()} (Max Seq Len: 64)")

        # Optimization: Use physical cores (6) instead of logical (12) to avoid contention
        num_workers = 6 
        print(f"  Starting multi-process pool (using {num_workers} physical cores)...")
        self.pool = self.model.start_multi_process_pool(target_devices=[self.device]*num_workers)

        os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

    def _ckpt_path(self, tag: str) -> str:
        return os.path.join(EMBEDDINGS_DIR, f"_ckpt_{tag}.json")

    def _load_ckpt(self, tag: str) -> dict | None:
        p = self._ckpt_path(tag)
        if os.path.exists(p):
            with open(p) as f:
                return json.load(f)
        return None

    def _save_ckpt(self, tag: str, data: dict):
        with open(self._ckpt_path(tag), "w") as f:
            json.dump(data, f, indent=2)

    def close(self):
        """Stop the multi-process pool."""
        if hasattr(self, "pool") and self.pool:
            print("\n Stopping multi-process pool...")
            self.model.stop_multi_process_pool(self.pool)

    def _encode_save(
        self,
        texts: list[str],
        page_ids: list[str],
        out_dir: str,
        chunk_id: int,
    ) -> int:
        # 1. TRUNCATION OPTIMIZATION:
        # We truncate to the first 256 characters. This is the biggest speed booster
        # because the model doesn't have to process long, redundant documents.
        truncated_texts = [t[:256] for t in texts]

        # 2. Use multi-processing for encoding
        emb = self.model.encode_multi_process(
            truncated_texts,
            self.pool,
            batch_size=ENCODE_BATCH_SIZE,
        )

        vecs = emb.astype(np.float32)
        path = os.path.join(out_dir, f"chunk_{chunk_id:04d}.npz")
        
        # L2 Normalize
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        vecs = vecs / (norms + 1e-10)

        path = os.path.join(out_dir, f"chunk_{chunk_id:04d}.npz")
        np.savez_compressed(
            path,
            vectors=vecs,
            page_ids=np.array(page_ids, dtype=object),
        )
        return vecs.shape[0]

    def process_non_http(self) -> int:
        out_dir = os.path.join(EMBEDDINGS_DIR, "non_http")
        os.makedirs(out_dir, exist_ok=True)

        ckpt = self._load_ckpt("non_http") or {
            "completed_files": [],
            "current_file": None,
            "lines_done": 0,
            "chunk_id": 0,
        }

        chunk_id   = ckpt.get("chunk_id", 0)
        total_vecs = 0

        for fname in NON_HTTP_FILES:
            if fname in ckpt["completed_files"]:
                print(f"  ⏭  {fname} (already done)")
                continue

            fpath = os.path.join(INPUT_DIR, fname)
            if not os.path.exists(fpath):
                print(f"{fname} not found — skipping")
                continue

            skip = ckpt["lines_done"] if ckpt["current_file"] == fname else 0

            print(f"\n{'─' * 60}")
            msg = f"  Embedding ▸ {fname}"
            if skip:
                msg += f"  (resuming from line {skip:,})"
            print(msg)
            print(f"{'─' * 60}")

            t0    = time.time()
            texts: list[str] = []
            pids:  list[str] = []
            lines = 0

            with open(fpath, "r", encoding="utf-8") as fh:
                for raw in fh:
                    if lines < skip:
                        lines += 1
                        continue
                    raw = raw.strip()
                    if not raw:
                        lines += 1
                        continue
                    try:
                        rec = _parse(raw)
                    except Exception:
                        lines += 1
                        continue

                    txt = rec.get("text", "")
                    if not txt:
                        lines += 1
                        continue

                    texts.append(txt)
                    pids.append(rec.get("page_id", ""))
                    lines += 1

                    if len(texts) >= CHUNK_SIZE:
                        n = self._encode_save(texts, pids, out_dir, chunk_id)
                        total_vecs += n
                        chunk_id   += 1

                        if INDEXING_LIMIT and total_vecs >= INDEXING_LIMIT:
                            print(f"\n  🛑 Reached INDEXING_LIMIT ({INDEXING_LIMIT:,}) — stopping.")
                            ckpt.update(
                                current_file=fname,
                                lines_done=lines,
                                chunk_id=chunk_id,
                            )
                            self._save_ckpt("non_http", ckpt)
                            return total_vecs

                        ckpt.update(
                            current_file=fname,
                            lines_done=lines,
                            chunk_id=chunk_id,
                        )
                        self._save_ckpt("non_http", ckpt)

                        elapsed = time.time() - t0
                        print(
                            f"    chunk {chunk_id:>4}  |  "
                            f"{lines:>10,} lines  |  "
                            f"{lines / elapsed:,.0f} l/s"
                        )
                        texts, pids = [], []

            if texts:
                n = self._encode_save(texts, pids, out_dir, chunk_id)
                total_vecs += n
                chunk_id   += 1

            ckpt["completed_files"].append(fname)
            ckpt.update(current_file=None, lines_done=0, chunk_id=chunk_id)
            self._save_ckpt("non_http", ckpt)
            print(f"  ✓ {fname} done  ({time.time() - t0:.1f}s)")

        print(f"\n  Total non-HTTP vectors: {total_vecs:,}")
        return total_vecs

    def process_http(self, start_total: int = 0) -> int:
        fpath = os.path.join(INPUT_DIR, HTTP_FILE)
        if not os.path.exists(fpath):
            print(f"{HTTP_FILE} not found!")
            return 0

        month_dirs: dict[str, str] = {}
        for m in HTTP_MONTHS:
            d = os.path.join(EMBEDDINGS_DIR, f"http_{m}")
            os.makedirs(d, exist_ok=True)
            month_dirs[m] = d

        ckpt = self._load_ckpt("http") or {
            "lines_done": 0,
            "month_chunks": {m: 0 for m in HTTP_MONTHS},
            "unknown_chunks": 0,
        }
        skip         = ckpt["lines_done"]
        month_chunks = ckpt["month_chunks"]

        print(f"\n{'═' * 60}")
        print("  Embedding ▸ HTTP  (monthly sharding)")
        if skip:
            print(f"  Resuming from line {skip:,}")
        print(f"{'═' * 60}")

        bufs: dict[str, dict] = {
            m: {"texts": [], "pids": []} for m in HTTP_MONTHS
        }
        unknown_buf: dict[str, list] = {"texts": [], "pids": []}

        t0         = time.time()
        lines      = 0
        total_vecs = 0

        file_size  = os.path.getsize(fpath)

        with open(fpath, "r", encoding="utf-8") as fh:
            while True:
                raw = fh.readline()
                if not raw:
                    break

                if lines < skip:
                    lines += 1
                    continue

                raw = raw.strip()
                if not raw:
                    lines += 1
                    continue
                try:
                    rec = _parse(raw)
                except Exception:
                    lines += 1
                    continue

                txt = rec.get("text", "")
                if not txt:
                    lines += 1
                    continue

                pid   = rec.get("page_id", "")
                dt    = rec.get("date", "")
                month = dt[:7] if dt and len(dt) >= 7 else None

                if month in bufs:
                    bufs[month]["texts"].append(txt)
                    bufs[month]["pids"].append(pid)

                    if len(bufs[month]["texts"]) >= CHUNK_SIZE:
                        n = self._encode_save(
                            bufs[month]["texts"],
                            bufs[month]["pids"],
                            month_dirs[month],
                            month_chunks[month],
                        )
                        total_vecs        += n
                        month_chunks[month] += 1
                        bufs[month]         = {"texts": [], "pids": []}

                        if INDEXING_LIMIT and (start_total + total_vecs) >= INDEXING_LIMIT:
                            print(f"\n  🛑 Reached INDEXING_LIMIT ({INDEXING_LIMIT:,}) — stopping.")
                            ckpt.update(lines_done=lines, month_chunks=month_chunks)
                            self._save_ckpt("http", ckpt)
                            return total_vecs

                        ckpt.update(lines_done=lines, month_chunks=month_chunks)
                        self._save_ckpt("http", ckpt)

                        elapsed = time.time() - t0
                        rate    = (lines - skip) / elapsed if elapsed else 0
                        print(
                            f"    {month} chunk {month_chunks[month]:>3}  |  "
                            f"lines {lines:>12,}  |  "
                            f"{rate:,.0f} l/s"
                        )
                else:
                    unknown_buf["texts"].append(txt)
                    unknown_buf["pids"].append(pid)

                lines += 1

                if lines % 500_000 == 0:
                    elapsed = time.time() - t0
                    rate    = (lines - skip) / elapsed if elapsed else 0
                    pos       = fh.tell()
                    remaining = max(0, file_size - pos)
                    avg_bpl   = pos / max(lines, 1)
                    rem_lines = remaining / avg_bpl if avg_bpl else 0
                    eta_min   = rem_lines / rate / 60 if rate else 0
                    print(
                        f"    progress {lines:>12,} lines  |  "
                        f"{rate:,.0f} l/s  |  "
                        f"ETA ~{eta_min:.0f} min"
                    )

        for m in HTTP_MONTHS:
            if bufs[m]["texts"]:
                n = self._encode_save(
                    bufs[m]["texts"], bufs[m]["pids"],
                    month_dirs[m], month_chunks[m],
                )
                total_vecs        += n
                month_chunks[m]   += 1

        if unknown_buf["texts"]:
            unk_dir = os.path.join(EMBEDDINGS_DIR, "http_unknown")
            os.makedirs(unk_dir, exist_ok=True)
            n = self._encode_save(
                unknown_buf["texts"], unknown_buf["pids"],
                unk_dir, ckpt.get("unknown_chunks", 0),
            )
            total_vecs += n

        ckpt.update(
            lines_done=lines,
            month_chunks=month_chunks,
            completed=True,
        )
        self._save_ckpt("http", ckpt)

        elapsed = time.time() - t0
        print(f"\n HTTP done: {total_vecs:,} vectors  |  "
              f"{lines:,} lines  |  {elapsed:.1f}s")
        for m in HTTP_MONTHS:
            print(f"      {m}: {month_chunks[m]} chunks")
        return total_vecs
