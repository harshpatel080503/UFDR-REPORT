import sys
import os
import json
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Retriever"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reranker"))

from Retriever.engine import RetrieverEngine

BANNER = r"""
+-------------------------------------------------------+
|        UFDR Copilot — Pipeline Orchestrator           |
+-------------------------------------------------------+
|  Input : User Query                                   |
|  Flow  : Retrieval (FAISS) -> Rerank (Cross-Encoder)  |
|  Goal  : Top 5 Refined Evidence                       |
+-------------------------------------------------------+
"""

def main():
    if len(sys.argv) < 2:
        print(BANNER)
        print("Usage: python run.py \"query string\"")
        sys.exit(1)

    query = sys.argv[1]
    
    try:
        engine = RetrieverEngine()
    except Exception as e:
        print(f"Error initializing pipeline components: {e}")
        sys.exit(1)

    print(f"\n[*] Processing Query: '{query}'")
    
    results, t_total, t_rerank = engine.search(query, k=50, use_reranker=True)
    
    top_5_evidence = results[:5]

    output = {
        "query": query,

        "metadata": {
            "retrieval_time_sec": round(t_total, 4),
            "rerank_time_sec": round(t_rerank, 4),
            "total_candidates_searched": 50,
            "final_evidence_count": len(top_5_evidence)
        },
        "evidence_set": []
    }

    for i, rec in enumerate(top_5_evidence, 1):
        evidence = {
            "rank": i,
            "page_id": rec.get("page_id"),
            "source": rec.get("source"),
            "timestamp": rec.get("date"),
            "user": rec.get("user"),
            "action": rec.get("action"),
            "text": rec.get("text"),
            "scores": {
                "faiss_distance": round(rec.get("_search_score", 0), 4),
                "rerank_score": round(rec.get("_rerank_score", 0), 4)
            }
        }
        output["evidence_set"].append(evidence)

    print("\n" + "="*80)
    print("   FINAL TOP 5 EVIDENCE (JSON OUTPUT)")
    print("="*80)
    print(json.dumps(output, indent=2))
    print("="*80 + "\n")

    engine.close()

if __name__ == "__main__":
    main()
