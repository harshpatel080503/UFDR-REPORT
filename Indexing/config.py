import os

BASE_DIR   = r"E:\Data Science Study\Deep Learning Project\UFDR"
INPUT_DIR  = os.path.join(BASE_DIR, "Data", "processed data", "PageIndex_Data")
OUTPUT_DIR = os.path.join(BASE_DIR, "Indexing", "output")

PAGEINDEX_DB   = os.path.join(OUTPUT_DIR, "page_index.db")
EMBEDDINGS_DIR = os.path.join(OUTPUT_DIR, "embeddings")
FAISS_DIR      = os.path.join(OUTPUT_DIR, "faiss")

NON_HTTP_FILES = [
    "email.jsonl",
    "logon.jsonl",
    "device.jsonl",
    "file.jsonl",
    "ldap.jsonl",
    "psychometric.jsonl",
]
HTTP_FILE = "http.jsonl"

EMBEDDING_MODEL   = r"E:\Data Science Study\Deep Learning Project\UFDR\Retriever\models\fine-tuned-minilm-20260509-214538"
EMBEDDING_DIM     = 384
ENCODE_BATCH_SIZE = 1024
CHUNK_SIZE        = 50_000       # records per saved embedding chunk
INDEXING_LIMIT    = None         # max total embeddings to generate (None = all)

FAISS_NLIST      = 1024          # IVF Voronoi cells
FAISS_M_PQ       = 48            # PQ sub-quantizers  (384 / 8)
FAISS_NBITS      = 8             # bits per sub-quantizer code
FAISS_TRAIN_SIZE = 250_000       # vectors sampled for IVF+PQ training
FAISS_MIN_IVF    = 10_000        # below this count → use Flat index

SQLITE_BATCH       = 100_000     # rows per INSERT commit
STORE_FULL_RECORD  = True        # keep raw JSON for the Retriever module

HTTP_MONTHS = [
    "2010-01", "2010-02", "2010-03",
    "2010-04", "2010-05", "2010-06",
]
