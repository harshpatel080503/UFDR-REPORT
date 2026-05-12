import os
import sys
from dotenv import load_dotenv

ROOT_DIR = r"e:\Data Science Study\Deep Learning Project\UFDR"
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Retriever"))

load_dotenv(os.path.join(ROOT_DIR, ".env"))

from Retriever.engine import RetrieverEngine

def find_real_logs():
    retriever = RetrieverEngine()
    
    scenarios = [
        ("wikileaks.org", "Data Exfiltration"),
        ("monster.com job search", "Insider Theft"),
        ("downloaded keylogger stealth tools", "Sabotage")
    ]
    
    for query, label in scenarios:
        print(f"\n--- {label} (Query: {query}) ---")
        results, _, _ = retriever.search(query, k=5)
        for r in results:
            print(f"User: {r['user']} | Date: {r['date']} | ID: {r['page_id']} | Text: {r['text'][:100]}")
            
    retriever.close()

if __name__ == "__main__":
    find_real_logs()
