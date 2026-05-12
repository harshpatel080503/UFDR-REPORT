import sqlite3
import json
import os
import random
import csv
from datetime import datetime

random.seed(42)

BASE = r"e:\Data Science Study\Deep Learning Project\UFDR"
DB_PATH = os.path.join(BASE, "Indexing", "output", "page_index.db")
INSIDERS_CSV = os.path.join(BASE, "Data", "processed data", "Insiders Ground Truth Labels", "insiders.csv")
OUTPUT = os.path.join(BASE, "Evaluation", "golden_dataset.json")

SCENARIO_META = {
    1: {"threat_category": "Data Exfiltration", "risk_score": 9, "description": "After-hours logon, removable drive, wikileaks.org uploads"},
    2: {"threat_category": "Insider Theft", "risk_score": 7, "description": "Job hunting on career sites, thumb-drive data theft before departure"},
    3: {"threat_category": "Sabotage", "risk_score": 10, "description": "Keylogger download, USB transfer to supervisor, impersonation email"},
}

def parse_date(d):
    for fmt in ("%m/%d/%Y %H:%M:%S", "%m/%d/%Y", "%Y-%m-%d"):
        try: return datetime.strptime(d.strip(), fmt)
        except: continue
    return None

def main():
    print("Starting golden dataset builder...", flush=True)
    conn = sqlite3.connect(DB_PATH)
    insiders = []
    try:
        with open(INSIDERS_CSV, "r") as f:
            for row in csv.DictReader(f):
                d = parse_date(row["start"])
                if d:
                    insiders.append({
                        "user": row["user"],
                        "scenario": int(row["scenario"]),
                        "start": d,
                        "end": parse_date(row["end"]) or d,
                    })
    except Exception as e:
        print(f"Error reading CSV: {e}", flush=True)

    # Filter for indexed range
    limit_date = datetime(2010, 6, 29)
    available = [i for i in insiders if i["start"] <= limit_date]
    print(f"Available insiders in range: {len(available)}", flush=True)
    
    if not available:
        available = insiders[:20] # fallback

    dataset = []
    qid = 1
    
    # Process them one by one
    for i in available:
        if qid > 100: break
        
        user = i["user"]
        s = i["start"].strftime("%Y-%m-%d")
        e = i["end"].strftime("%Y-%m-%d")
        
        cursor = conn.cursor()
        cursor.execute("SELECT page_id FROM documents WHERE user = ? AND date >= ? AND date <= ? LIMIT 5", (user, s, e))
        page_ids = [r[0] for r in cursor.fetchall()]
        
        if not page_ids:
            # Try any logs for this user
            cursor.execute("SELECT page_id FROM documents WHERE user = ? LIMIT 5", (user,))
            page_ids = [r[0] for r in cursor.fetchall()]
            
        if not page_ids: continue
        
        scenario_id = i["scenario"]
        meta = SCENARIO_META.get(scenario_id, SCENARIO_META[1])
        
        # Create 9-10 queries per insider to reach 100
        for _ in range(10):
            if qid > 100: break
            
            # Simple query with dates
            query = f"Investigate {meta['threat_category']} for user {user} from {s} to {e}."
            summary = f"User {user} was involved in {meta['threat_category']} between {s} and {e} ({meta['description']})."
            
            dataset.append({
                "query_id": f"Q{qid:03d}",
                "query": query,
                "expected_log_ids": page_ids,
                "expected_threat_category": meta["threat_category"],
                "expected_risk_score": meta["risk_score"],
                "ideal_summary": summary,
                "scenario": scenario_id,
                "insider_user": user,
            })
            qid += 1
            
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Done. Saved {len(dataset)} queries.")
    conn.close()

if __name__ == "__main__":
    main()
