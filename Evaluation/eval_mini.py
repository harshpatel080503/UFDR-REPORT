import os
import sys
import json
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Retriever"))

from Retriever.engine import RetrieverEngine
from Evaluation.eval_retriever import evaluate_retriever

def run_mini_eval():
    with open(os.path.join(ROOT_DIR, "Evaluation", "golden_dataset.json"), "r") as f:
        dataset = json.load(f)[:5] # Just first 5
        
    print(f"[*] Running mini-eval on {len(dataset)} examples...")
    retriever = RetrieverEngine()
    metrics = evaluate_retriever(retriever, dataset, k=10, use_reranker=True)
    
    print("\n" + "="*30)
    print("   MINI-EVAL RESULTS")
    print("="*30)
    print(json.dumps(metrics, indent=4))
    retriever.close()

if __name__ == "__main__":
    run_mini_eval()
