import time
from sentence_transformers import CrossEncoder

from reranker_config import (
    RERANK_MODEL,
    RERANK_DEVICE,
    RERANK_BATCH_SIZE,
)

class RerankEngine:
    def __init__(self):
        print(f"  Loading Reranker model ({RERANK_MODEL}) ...")
        self.model = CrossEncoder(RERANK_MODEL, device=RERANK_DEVICE)
        print("  [+] Reranker ready.")

    def rerank(self, query: str, records: list):
        if not records:
            return [], 0.0

        t0 = time.time()
        
        pairs = [[query, r.get("text", "")] for r in records]
        
        scores = self.model.predict(
            pairs, 
            batch_size=RERANK_BATCH_SIZE, 
            show_progress_bar=False
        )
        
        for i, score in enumerate(scores):
            records[i]["_rerank_score"] = float(score)
            
        records.sort(key=lambda x: x["_rerank_score"], reverse=True)
        
        elapsed = time.time() - t0
        return records, elapsed