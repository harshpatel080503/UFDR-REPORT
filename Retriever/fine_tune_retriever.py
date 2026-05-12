import os
import json
import torch
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from datetime import datetime

# Configuration
BASE_DIR = r"E:\Data Science Study\Deep Learning Project\UFDR"
TRAIN_DATA_PATH = os.path.join(BASE_DIR, "Data", "synthetic_train_data.jsonl")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
OUTPUT_PATH = os.path.join(BASE_DIR, "Retriever", "models", f"fine-tuned-minilm-{datetime.now().strftime('%Y%m%d-%H%M%S')}")

# Training Hyperparameters
BATCH_SIZE = 16  # Adjust based on VRAM (8-16 is safe for 4GB)
EPOCHS = 3
WARMUP_STEPS = 50

def load_examples(path):
    examples = []
    with open(path, "r") as f:
        for line in f:
            data = json.loads(line)
            # MultipleNegativesRankingLoss only needs positive pairs
            if float(data.get("label", 1.0)) == 1.0:
                examples.append(InputExample(texts=[data["query"], data["positive_text"]]))
    return examples

def main():
    print("\n" + "="*50)
    print("   RETRIEVER FINE-TUNING STARTING")
    print("="*50)
    
    if not os.path.exists(TRAIN_DATA_PATH):
        print(f"  [!] ERROR: Training data not found at {TRAIN_DATA_PATH}")
        print("      Please run Evaluation/generate_synthetic_data.py first.")
        return

    print(f"  [+] Loading model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    
    # Check for GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    print(f"  [+] Using device: {device}")

    print(f"  [+] Loading training data from {TRAIN_DATA_PATH}...")
    train_examples = load_examples(TRAIN_DATA_PATH)
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=BATCH_SIZE)
    
    # Loss function: MultipleNegativesRankingLoss
    # This loss treats every other positive in the batch as a negative.
    train_loss = losses.MultipleNegativesRankingLoss(model=model)

    print("Starting training...")
    # Fine-tune the model
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=EPOCHS,
        warmup_steps=WARMUP_STEPS,
        output_path=OUTPUT_PATH,
        use_amp=True if device == "cuda" else False, # Automatic Mixed Precision for GPU
        show_progress_bar=True
    )

    print(f"\nTraining complete! Model saved to: {OUTPUT_PATH}")
    
    # Create a symlink or simple pointer for the config to use
    latest_path = os.path.join(BASE_DIR, "Retriever", "models", "fine-tuned-minilm-latest")
    # On Windows, we'll just print instructions to update config or use a fixed path
    print(f"Update your retriever_config.py to use this path.")

if __name__ == "__main__":
    main()
