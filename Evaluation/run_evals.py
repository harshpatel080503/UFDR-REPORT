import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Adjust paths to import from root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Retriever"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reranker"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reasoning"))

# Load environment variables
load_dotenv(os.path.join(ROOT_DIR, ".env"))

try:
    from Retriever.engine import RetrieverEngine
    from Reasoning.reasoner import ReasoningEngine
    from eval_retriever import evaluate_retriever
    from eval_generator import evaluate_generator
except ImportError as e:
    print(f"[!] Import Error: {e}")
    print("Ensure you are running this from the Evaluation directory or the root directory.")
    sys.exit(1)

DATASET_PATH = os.path.join(os.path.dirname(__file__), "golden_dataset.json")

def load_dataset(path):
    if not os.path.exists(path):
        print(f"[!] Dataset not found at {path}")
        return []
    with open(path, "r") as f:
        return json.load(f)

def run_all_evaluations():
    print("="*60)
    print("   UFDR Baseline Quantitative Evaluation Suite")
    print("="*60)
    
    dataset = load_dataset(DATASET_PATH)
    if not dataset:
        print("[!] Cannot run evaluations without a dataset.")
        return

    print(f"[*] Loaded Golden Dataset with {len(dataset)} examples.")
    
    print("\n[*] Initializing Engines...")
    # NOTE: These might take a moment to load depending on hardware
    try:
        retriever = RetrieverEngine()
    except Exception as e:
        print(f"[!] Warning: Could not initialize RetrieverEngine: {e}")
        retriever = None

    try:
        reasoner = ReasoningEngine()
    except Exception as e:
        print(f"[!] Warning: Could not initialize ReasoningEngine: {e}")
        reasoner = None
        
    report = {
        "timestamp": datetime.now().isoformat(),
        "num_examples": len(dataset),
        "retriever_metrics": {},
        "generator_metrics": {}
    }

    # 1. Evaluate Retriever (Information Retrieval Metrics)
    if retriever:
        retriever_metrics = evaluate_retriever(retriever, dataset, k=10, use_reranker=True)
        report["retriever_metrics"] = retriever_metrics
    else:
        print("\n[!] Skipping Retriever Evaluation (Engine not loaded)")

    # 2. Evaluate Generator (Task & Grounding Metrics)
    if reasoner:
        # We pass the retriever to fetch real evidence, otherwise it uses mocked evidence
        generator_metrics = evaluate_generator(reasoner, dataset, retriever=retriever)
        report["generator_metrics"] = generator_metrics
    else:
        print("\n[!] Skipping Generator Evaluation (Engine not loaded)")

    # Output Final Report
    print("\n" + "="*60)
    print("   EVALUATION REPORT")
    print("="*60)
    print(json.dumps(report, indent=4))
    
    report_path = os.path.join(os.path.dirname(__file__), "baseline_metrics_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)
    print(f"\n[*] Full report saved to {report_path}")

if __name__ == "__main__":
    run_all_evaluations()
