import os
import sys
import json
from dotenv import load_dotenv

ROOT_DIR = r"e:\Data Science Study\Deep Learning Project\UFDR"
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Retriever"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reasoning"))

load_dotenv(os.path.join(ROOT_DIR, ".env"))

from Reasoning.reasoner import ReasoningEngine
from Retriever.engine import RetrieverEngine

def debug_generator():
    with open(os.path.join(ROOT_DIR, "Evaluation", "golden_dataset.json"), "r") as f:
        dataset = json.load(f)
    
    retriever = RetrieverEngine()
    reasoner = ReasoningEngine()
    
    print(f"{'Query ID':<10} | {'Expected':<20} | {'Predicted':<20} | {'Match'}")
    print("-" * 65)
    
    for item in dataset[:10]:
        query = item["query"]
        expected = item["expected_threat_category"]
        
        results, _, _ = retriever.search(query, k=10, use_reranker=True)
        analysis = reasoner.analyze(query, results)
        
        predicted = analysis.get("threat_category", "N/A")
        match = expected.lower() == str(predicted).lower()
        
        print(f"{item['query_id']:<10} | {expected:<20} | {predicted:<20} | {match}")
        
    retriever.close()

if __name__ == "__main__":
    debug_generator()
