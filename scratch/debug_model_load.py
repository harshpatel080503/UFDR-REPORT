import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

print("--- DEBUG SCRIPT STARTING (CPU ONLY) ---")
import torch
print(f"Torch imported, CUDA available: {torch.cuda.is_available()}")
import sentence_transformers
print("sentence_transformers package imported")
