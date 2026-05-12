import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

print("--- DEBUG SCRIPT STARTING (CPU ONLY + LOAD MODEL) ---")
import torch
from sentence_transformers import SentenceTransformer

model_path = r"E:\Data Science Study\Deep Learning Project\UFDR\Retriever\models\fine-tuned-minilm-20260509-214538"
print(f"Loading model from: {model_path}")

try:
    model = SentenceTransformer(model_path, device="cpu")
    print("SUCCESS: Model loaded on CPU!")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
