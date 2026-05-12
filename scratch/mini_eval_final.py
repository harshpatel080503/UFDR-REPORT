import os
import sys
import json
from dotenv import load_dotenv

ROOT_DIR = r"e:\Data Science Study\Deep Learning Project\UFDR"
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Retriever"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reasoning"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Evaluation"))

load_dotenv(os.path.join(ROOT_DIR, ".env"))

from Retriever.engine import RetrieverEngine
from Reasoning.reasoner import ReasoningEngine
from eval_generator import evaluate_generator
from eval_retriever import evaluate_retriever

def run_mini_eval():
    with open(os.path.join(ROOT_DIR, "Evaluation", "golden_dataset.json"), "r") as f:
        dataset = json.load(f)[:5]
        
    retriever = RetrieverEngine()
    reasoner = ReasoningEngine()
    
    print("\n--- MINI EVAL (5 QUERIES) ---")
    ret_metrics = evaluate_retriever(retriever, dataset, k=10, use_reranker=True)
    gen_metrics = evaluate_generator(reasoner, dataset, retriever=retriever)
    
    print("\nRETRIEVER:", json.dumps(ret_metrics, indent=2))
    print("GENERATOR:", json.dumps(gen_metrics, indent=2))
    
    retriever.close()

if __name__ == "__main__":
    run_mini_eval()
