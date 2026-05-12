import numpy as np

def calculate_mrr(retrieved_ids, expected_ids):
    """Calculate Mean Reciprocal Rank for a single query."""
    for i, rid in enumerate(retrieved_ids):
        if rid in expected_ids:
            return 1.0 / (i + 1)
    return 0.0

def calculate_recall_at_k(retrieved_ids, expected_ids, k):
    """Calculate Recall@K for a single query."""
    retrieved_k = retrieved_ids[:k]
    hits = sum(1 for eid in expected_ids if eid in retrieved_k)
    return hits / len(expected_ids) if expected_ids else 0.0

def calculate_ndcg_at_k(retrieved_ids, expected_ids, k):
    """Calculate NDCG@K for a single query."""
    retrieved_k = retrieved_ids[:k]
    dcg = 0.0
    for i, rid in enumerate(retrieved_k):
        if rid in expected_ids:
            rel = 1.0 # Assuming binary relevance
            dcg += (2**rel - 1) / np.log2(i + 2)
            
    idcg = 0.0
    for i in range(min(k, len(expected_ids))):
        rel = 1.0
        idcg += (2**rel - 1) / np.log2(i + 2)
        
    return dcg / idcg if idcg > 0 else 0.0

def evaluate_retriever(retriever, dataset, k=10, use_reranker=True):
    """
    Evaluate the Retriever/Reranker on the golden dataset.
    """
    metrics = {
        f"mrr": [],
        f"recall@{k}": [],
        f"ndcg@{k}": []
    }
    
    print(f"\n[+] Evaluating Retriever (k={k}, reranker={use_reranker})...")
    
    for item in dataset:
        query = item["query"]
        expected_ids = item.get("expected_log_ids", [])
        
        if not expected_ids:
            continue
            
        results, _, _ = retriever.search(query, k=k, use_reranker=use_reranker)
        retrieved_ids = [str(r.get("page_id", r.get("id", ""))) for r in results]
        
        mrr = calculate_mrr(retrieved_ids, expected_ids)
        recall = calculate_recall_at_k(retrieved_ids, expected_ids, k)
        ndcg = calculate_ndcg_at_k(retrieved_ids, expected_ids, k)
        
        metrics["mrr"].append(mrr)
        metrics[f"recall@{k}"].append(recall)
        metrics[f"ndcg@{k}"].append(ndcg)
        
    # Aggregate
    agg_metrics = {k: np.mean(v) if v else 0.0 for k, v in metrics.items()}
    return agg_metrics
