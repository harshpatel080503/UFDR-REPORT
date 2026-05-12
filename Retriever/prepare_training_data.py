import os
import json
import sqlite3
import random
from tqdm import tqdm

# Configuration
BASE_DIR = r"E:\Data Science Study\Deep Learning Project\UFDR"
GOLDEN_DATASET_PATH = os.path.join(BASE_DIR, "Evaluation", "golden_dataset.json")
DB_PATH = os.path.join(BASE_DIR, "Indexing", "output", "page_index.db")
OUTPUT_RETRIEVER = os.path.join(BASE_DIR, "Retriever", "retriever_train.jsonl")
OUTPUT_RERANKER = os.path.join(BASE_DIR, "Reranker", "reranker_train.jsonl")

def fetch_texts(log_ids):
    if not log_ids:
        return {}
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Batch fetching
    placeholders = ",".join("?" for _ in log_ids)
    query = f"SELECT page_id, text FROM documents WHERE page_id IN ({placeholders})"
    
    cursor.execute(query, list(log_ids))
    rows = cursor.fetchall()
    conn.close()
    
    return {row["page_id"]: row["text"] for row in rows}

def main():
    print(f"Loading golden dataset from {GOLDEN_DATASET_PATH}...")
    with open(GOLDEN_DATASET_PATH, "r") as f:
        golden_data = json.load(f)
    
    # 1. Collect all unique log IDs
    all_log_ids = set()
    for item in golden_data:
        all_log_ids.update(item.get("expected_log_ids", []))
    
    print(f"Found {len(all_log_ids)} unique positive log IDs.")
    
    # 2. Fetch texts from DB
    print("Fetching texts from SQLite...")
    log_id_to_text = fetch_texts(all_log_ids)
    print(f"Successfully fetched {len(log_id_to_text)} texts.")
    
    # 3. Prepare Retriever Training Data (Triplets: Query, Positive, Negative)
    # Since we don't have many negatives yet, we'll use MultipleNegativesRankingLoss 
    # which treats other positives in the batch as negatives.
    retriever_triplets = []
    reranker_samples = []
    
    for item in golden_data:
        query = item["query"]
        positives = item.get("expected_log_ids", [])
        
        for pos_id in positives:
            pos_text = log_id_to_text.get(pos_id)
            if pos_text:
                # Retriever format: [query, positive]
                retriever_triplets.append({"query": query, "positive": pos_text})
                
                # Reranker format: [query, text, label]
                reranker_samples.append({"query": query, "text": pos_text, "label": 1})
    
    # 4. Save Retriever Data
    print(f"Saving {len(retriever_triplets)} retriever samples to {OUTPUT_RETRIEVER}...")
    with open(OUTPUT_RETRIEVER, "w") as f:
        for entry in retriever_triplets:
            f.write(json.dumps(entry) + "\n")
            
    # 5. Save Reranker Data
    print(f"Saving {len(reranker_samples)} reranker samples to {OUTPUT_RERANKER}...")
    with open(OUTPUT_RERANKER, "w") as f:
        for entry in reranker_samples:
            f.write(json.dumps(entry) + "\n")

    print("\nDone! Training data prepared.")

if __name__ == "__main__":
    main()
