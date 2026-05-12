import os
import sys
import json
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Retriever"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reranker"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reasoning"))

from Retriever.engine import RetrieverEngine
from Reasoning.reasoner import ReasoningEngine
from Evaluation.eval_retriever import evaluate_retriever
from Evaluation.eval_generator import evaluate_generator

def run_verified_eval():
    with open(os.path.join(ROOT_DIR, "Evaluation", "golden_dataset.json"), "r") as f:
        dataset = json.load(f)[:10] # 10 queries
        
    print(f"[*] Running verified evaluation on {len(dataset)} examples...")
    retriever = RetrieverEngine()
    reasoner = ReasoningEngine()
    
    # 1. Retriever Metrics
    ret_metrics = evaluate_retriever(retriever, dataset, k=10, use_reranker=True)
    
    # 2. Generator Metrics
    gen_metrics = evaluate_generator(reasoner, dataset, retriever=retriever)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "num_examples": len(dataset),
        "retriever_metrics": ret_metrics,
        "generator_metrics": gen_metrics
    }
    
    print("\n" + "="*40)
    print("   VERIFIED EVALUATION REPORT (n=10)")
    print("="*40)
    print(json.dumps(report, indent=4))
    
    retriever.close()

if __name__ == "__main__":
    run_verified_eval()
