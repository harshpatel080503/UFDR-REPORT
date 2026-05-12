import os
import glob
import time

import numpy as np
import faiss

from config import (
    EMBEDDINGS_DIR,
    FAISS_DIR,
    EMBEDDING_DIM,
    FAISS_NLIST,
    FAISS_M_PQ,
    FAISS_NBITS,
    FAISS_TRAIN_SIZE,
    FAISS_MIN_IVF,
    HTTP_MONTHS,
)


class FAISSBuilder:

    def __init__(self):
        os.makedirs(FAISS_DIR, exist_ok=True)

    # ──────────────────────────────────────────────
    #  Core: chunk directory → .index + _ids.npy
    # ──────────────────────────────────────────────

    def build_from_chunks(self, chunk_dir: str, index_name: str):
        chunks = sorted(glob.glob(os.path.join(chunk_dir, "chunk_*.npz")))
        if not chunks:
            print(f"No chunks in {chunk_dir}")
            return None

        print(f"\n{'─' * 60}")
        print(f"  FAISS ▸ {index_name}   ({len(chunks)} chunk files)")
        print(f"{'─' * 60}")
        total = 0
        for p in chunks:
            with np.load(p, allow_pickle=True) as d:
                total += d["vectors"].shape[0]
        print(f"  Total vectors : {total:,}")

        if total < FAISS_MIN_IVF:
            print(f"  Index type    : IndexFlatL2  (small dataset)")
            index = faiss.IndexFlatL2(EMBEDDING_DIM)
        else:
            nlist = min(FAISS_NLIST, max(16, total // 40))
            print(f"  Index type    : IndexIVFPQ")
            print(f"    nlist={nlist}  m={FAISS_M_PQ}  nbits={FAISS_NBITS}")
            quantizer = faiss.IndexFlatL2(EMBEDDING_DIM)
            index = faiss.IndexIVFPQ(
                quantizer, EMBEDDING_DIM,
                nlist, FAISS_M_PQ, FAISS_NBITS,
            )
            index.nprobe = min(64, max(8, nlist // 4))

            n_sample = min(FAISS_TRAIN_SIZE, total)
            train_vecs = self._sample_vectors(chunks, n_sample)
            print(f"  Training on {train_vecs.shape[0]:,} sampled vectors …")
            t0 = time.time()
            faiss.normalize_L2(train_vecs)
            index.train(train_vecs)
            print(f" Trained in {time.time() - t0:.1f}s")
            del train_vecs

        all_ids: list = []
        added = 0
        t0 = time.time()

        for ci, cp in enumerate(chunks):
            with np.load(cp, allow_pickle=True) as data:
                vecs = data["vectors"].astype(np.float32)
                pids = data["page_ids"]

            faiss.normalize_L2(vecs)
            index.add(vecs)
            all_ids.extend(pids.tolist())
            added += vecs.shape[0]

            if (ci + 1) % 10 == 0 or ci == len(chunks) - 1:
                print(
                    f"    chunks {ci + 1:>4}/{len(chunks)}  |  "
                    f"{added:>10,} vectors added"
                )

        idx_path = os.path.join(FAISS_DIR, f"{index_name}.index")
        ids_path = os.path.join(FAISS_DIR, f"{index_name}_ids.npy")

        faiss.write_index(index, idx_path)
        np.save(ids_path, np.array(all_ids, dtype=object))

        size_mb = os.path.getsize(idx_path) / (1024 ** 2)
        elapsed = time.time() - t0
        print(
            f"  Saved  {idx_path}\n"
            f"           {size_mb:.1f} MB   |   {elapsed:.1f}s"
        )
        return index

    def _sample_vectors(
        self,
        chunk_paths: list[str],
        n_sample: int,
    ) -> np.ndarray:
        sizes: list[int] = []
        for cp in chunk_paths:
            with np.load(cp, allow_pickle=True) as d:
                sizes.append(d["vectors"].shape[0])
        total = sum(sizes)

        if total <= n_sample:
            parts = []
            for cp in chunk_paths:
                with np.load(cp, allow_pickle=True) as d:
                    parts.append(d["vectors"])
            return np.vstack(parts).astype(np.float32)

        rng     = np.random.default_rng(42)
        samples: list[np.ndarray] = []

        for cp, sz in zip(chunk_paths, sizes):
            n_from = max(1, int(n_sample * sz / total))
            with np.load(cp, allow_pickle=True) as d:
                vecs = d["vectors"]
            if n_from >= sz:
                samples.append(vecs)
            else:
                idx = rng.choice(sz, n_from, replace=False)
                samples.append(vecs[idx])

        result = np.vstack(samples).astype(np.float32)

        if result.shape[0] > n_sample:
            idx = rng.choice(result.shape[0], n_sample, replace=False)
            result = result[idx]

        return result


    def build_non_http(self):
        chunk_dir = os.path.join(EMBEDDINGS_DIR, "non_http")
        return self.build_from_chunks(chunk_dir, "non_http")

    def build_http_shards(self):
        for month in HTTP_MONTHS:
            chunk_dir = os.path.join(EMBEDDINGS_DIR, f"http_{month}")
            if os.path.isdir(chunk_dir) and any(
                f.endswith(".npz") for f in os.listdir(chunk_dir)
            ):
                self.build_from_chunks(chunk_dir, f"http_{month}")
            else:
                print(f"  ⏭  http_{month} — no chunks found")

        unk_dir = os.path.join(EMBEDDINGS_DIR, "http_unknown")
        if os.path.isdir(unk_dir) and any(
            f.endswith(".npz") for f in os.listdir(unk_dir)
        ):
            self.build_from_chunks(unk_dir, "http_unknown")

    def build_all(self):
        self.build_non_http()
        self.build_http_shards()

class FAISSSearcher:

    def __init__(self, index_name: str):
        idx_path = os.path.join(FAISS_DIR, f"{index_name}.index")
        ids_path = os.path.join(FAISS_DIR, f"{index_name}_ids.npy")

        if not os.path.exists(idx_path):
            raise FileNotFoundError(f"FAISS index not found: {idx_path}")

        self.index    = faiss.read_index(idx_path)
        self.page_ids = np.load(ids_path, allow_pickle=True)
        self.name     = index_name

    def search(
        self,
        query_vec: np.ndarray,
        k: int = 10,
    ) -> tuple[list[str], np.ndarray]:
        if query_vec.ndim == 1:
            query_vec = query_vec.reshape(1, -1)
        query_vec = query_vec.astype(np.float32)
        faiss.normalize_L2(query_vec)

        distances, indices = self.index.search(query_vec, k)

        valid     = indices[0] >= 0
        result_ids = [
            self.page_ids[i] if valid[j] else None
            for j, i in enumerate(indices[0])
        ]
        return result_ids, distances[0]
