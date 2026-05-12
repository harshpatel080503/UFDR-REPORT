import os
import json
import sqlite3
import random
from tqdm import tqdm
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "meta-llama/llama-3.1-8b-instruct"

# Configuration
BASE_DIR = r"E:\Data Science Study\Deep Learning Project\UFDR"
DB_PATH = os.path.join(BASE_DIR, "Indexing", "output", "page_index.db")
OUTPUT_PATH = os.path.join(BASE_DIR, "Data", "synthetic_train_data.jsonl")

def generate_queries_for_doc(doc, attempt_limit=3):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/OpenRouterTeam/openrouter-runner", # Required by OpenRouter
        "X-Title": "UFDR Synthetic Generator"
    }
    prompt = f"""
    You are a Senior Forensic Investigator. Below is a log entry from a corporate network.
    
    LOG ENTRY:
    User: {doc['user']} | Date: {doc['date']} | Type: {doc['event_type']}
    Content: {doc['text']}
    
    TASK:
    Generate exactly 3 distinct forensic queries that someone would ask to find THIS SPECIFIC log entry.
    - Query 1: A direct search (e.g., "Find emails sent by {doc['user']} on {doc['date']}")
    - Query 2: A reasoning-based search (e.g., "Identify potential data exfiltration activity involving {doc['user']}")
    - Query 3: An ambiguous human-like search (e.g., "What was {doc['user']} doing on the morning of the 15th that looked suspicious?")
    
    Output your response as a valid JSON list of strings. Example: ["query 1", "query 2", "query 3"]
    Do not include any other text, only the JSON.
    """
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    
    for attempt in range(attempt_limit):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            
            if response.status_code == 429:
                import time
                time.sleep(5 * (attempt + 1))
                continue
                
            response.raise_for_status()
            res_data = response.json()
            content = res_data['choices'][0]['message']['content']
            
            # OpenRouter sometimes returns the whole object if you ask for JSON
            # We try to parse the content which should be the JSON string
            data = json.loads(content)
            # If the LLM wrapped it in a key, extract it
            if isinstance(data, dict):
                for val in data.values():
                    if isinstance(val, list): return val
            return data
        except Exception as e:
            if attempt < attempt_limit - 1:
                import time
                time.sleep(1)
            else:
                return []
    return []

def get_hard_negative(doc, conn):
    """Find a document that is similar (same user or type) but is NOT the same document.
    Optimized: Avoids ORDER BY RANDOM() which is extremely slow on large tables."""
    cursor = conn.cursor()
    
    # Try to find docs from the same user but different ID (limit to 10 for speed)
    cursor.execute("""
        SELECT page_id, text FROM documents 
        WHERE user = ? AND page_id != ? 
        LIMIT 10
    """, (doc['user'], doc['page_id']))
    rows = cursor.fetchall()
    
    if not rows:
        # Fallback: find docs of the same event type (limit to 10 for speed)
        cursor.execute("""
            SELECT page_id, text FROM documents 
            WHERE event_type = ? AND page_id != ? 
            LIMIT 10
        """, (doc['event_type'], doc['page_id']))
        rows = cursor.fetchall()
        
    if rows:
        # Pick one randomly from the small result set
        row = random.choice(rows)
        return {"id": row[0], "text": row[1]}
    return None

def get_random_documents(n=250):
    """Blazing fast sampling using rowid."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT MIN(rowid), MAX(rowid) FROM documents")
    min_id, max_id = cursor.fetchone()
    
    documents = []
    seen_ids = set()
    
    while len(documents) < n:
        rid = random.randint(min_id, max_id)
        if rid in seen_ids: continue
        
        cursor.execute("SELECT page_id, text, user, date, event_type FROM documents WHERE rowid = ?", (rid,))
        row = cursor.fetchone()
        if row:
            documents.append({
                "page_id": row[0],
                "text": row[1],
                "user": row[2],
                "date": row[3],
                "event_type": row[4]
            })
            seen_ids.add(rid)
    return documents, conn

import concurrent.futures
from threading import Lock

write_lock = Lock()

def process_doc_with_neg(doc, hard_neg):
    """Worker function to generate queries for a single doc with its pre-fetched hard negative."""
    queries = generate_queries_for_doc(doc)
    
    results = []
    for q in queries:
        entry = {
            "query": q,
            "positive_id": doc["page_id"],
            "positive_text": doc["text"],
            "label": 1.0,
            "metadata": {
                "user": doc["user"],
                "date": doc["date"],
                "type": doc["event_type"]
            }
        }
        results.append(entry)
        
        if hard_neg:
            neg_entry = entry.copy()
            neg_entry["positive_id"] = hard_neg["id"]
            neg_entry["positive_text"] = hard_neg["text"]
            neg_entry["label"] = 0.0
            results.append(neg_entry)
    return results

def main():
    target_count = 250
    print(f"Sampling {target_count} documents and hard negatives from database...")
    docs, conn = get_random_documents(target_count)
    
    # Pre-fetch hard negatives to avoid SQLite thread issues
    prepared_data = []
    for doc in tqdm(docs, desc="Pre-fetching"):
        hard_neg = get_hard_negative(doc, conn)
        prepared_data.append((doc, hard_neg))
    conn.close()
    
    print(f"\nGenerating synthetic queries using {MODEL_NAME} in PARALLEL (Max Workers: 10)...")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Start fresh
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
        
    count = 0
    # Use ThreadPoolExecutor for parallel API calls
    with open(OUTPUT_PATH, "a") as f:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Map the process_doc_with_neg function
            future_to_doc = {executor.submit(process_doc_with_neg, d[0], d[1]): d for d in prepared_data}
            
            for future in tqdm(concurrent.futures.as_completed(future_to_doc), total=len(prepared_data), desc="Generating"):
                doc_results = future.result()
                if doc_results:
                    with write_lock:
                        for entry in doc_results:
                            f.write(json.dumps(entry) + "\n")
                            count += 1
                        f.flush()
    
    print(f"\nSuccessfully generated ~{count} synthetic samples (Positives + Hard Negatives).")
    print(f"Saved synthetic training data to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
