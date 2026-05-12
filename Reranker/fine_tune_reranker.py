import os
import json
import torch
from torch.utils.data import DataLoader
from sentence_transformers import CrossEncoder, InputExample, losses
from sentence_transformers.cross_encoder.evaluation import CECorrelationEvaluator
from datetime import datetime

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_DATA_PATH = os.path.join(BASE_DIR, "Data", "synthetic_train_data.jsonl")
MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
OUTPUT_PATH = os.path.join(BASE_DIR, "Reranker", "models_reranker")

# Training Hyperparameters
BATCH_SIZE = 8 # Cross-Encoders are heavier than Bi-Encoders
EPOCHS = 3

def load_examples(path):
    examples = []
    with open(path, "r") as f:
        for line in f:
            data = json.loads(line)
            # Label is 1 for positive, 0 for negative (from synthetic data)
            examples.append(InputExample(texts=[data["query"], data["positive_text"]], label=float(data.get("label", 1.0))))
    return examples

def main():
    print(f"Loading model: {MODEL_NAME}...")
    # Check for GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CrossEncoder(MODEL_NAME, device=device)
    print(f"Using device: {device}")

    print(f"Loading training data from {TRAIN_DATA_PATH}...")
    train_examples = load_examples(TRAIN_DATA_PATH)
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=BATCH_SIZE)
    
    # Pre-flight check: Can we actually write to this drive?
    print(f"Checking write permissions for {OUTPUT_PATH}...")
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    try:
        test_file = os.path.join(OUTPUT_PATH, "write_test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print("Pre-flight check passed!")
    except Exception as e:
        print(f"CRITICAL ERROR: Pre-flight write check failed! {e}")
        return
    
    # We don't need to specify a loss for CrossEncoder.fit, it uses CrossEntropyLoss by default for classification
    
    print(f"Starting training on {device}...")
    # Create directory upfront to avoid any path issues
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    model.fit(
        train_dataloader=train_dataloader,
        epochs=EPOCHS,
        output_path=OUTPUT_PATH,
        show_progress_bar=True
    )
    
    # Force an explicit save in case model.fit's internal save was interrupted
    print("Performing explicit secondary save...")
    model.save(OUTPUT_PATH)

    print(f"\nTraining complete! Model saved to: {OUTPUT_PATH}")
    
    # Verification Step
    if os.path.exists(OUTPUT_PATH):
        print(f"Verified! Contents of {OUTPUT_PATH}:")
        for f in os.listdir(OUTPUT_PATH):
            print(f"  - {f}")
    else:
        print(f"CRITICAL ERROR: {OUTPUT_PATH} does not exist even after saving!")

if __name__ == "__main__":
    main()
