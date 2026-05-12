import os
# Use relative path to avoid space issues
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RERANK_MODEL = os.path.join(ROOT_DIR, "Reranker", "models_reranker")
RERANK_DEVICE = "cpu"
RERANK_BATCH_SIZE = 32

TOP_K_INITIAL = 100
TOP_K_FINAL = 50
RERANK_DEPTH = 50
