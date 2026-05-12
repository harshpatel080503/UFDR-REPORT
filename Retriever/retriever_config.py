import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Indexing"))

from Indexing.config import (
    OUTPUT_DIR,
    FAISS_DIR,
    PAGEINDEX_DB,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
)

RETRIEVER_K = 10
SEARCH_DEVICE = "cpu"
SCORE_THRESHOLD = 0.5

DISPLAY_COLS = ["date", "user", "action", "text"]
TEXT_WRAP_WIDTH = 80
