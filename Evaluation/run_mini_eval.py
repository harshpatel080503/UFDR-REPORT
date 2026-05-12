import os
import sys
import shutil
import subprocess

# Paths
BASE_DIR = r"E:\Data Science Study\Deep Learning Project\UFDR"
CONFIG_PATH = os.path.join(BASE_DIR, "Indexing", "config.py")
FAISS_DIR_MINI = os.path.join(BASE_DIR, "Indexing", "output", "faiss_mini")

# Mini files from reindex
MINI_INDEX = os.path.join(BASE_DIR, "Evaluation", "mini_eval.index")
MINI_IDS = os.path.join(BASE_DIR, "Evaluation", "mini_eval_ids.npy")

def main():
    print("\n" + "="*60)
    print("  UFDR MINI-EVALUATION WRAPPER")
    print("="*60)

    # 1. Setup Mini Folder
    print(f"[*] Setting up mini FAISS directory...")
    os.makedirs(FAISS_DIR_MINI, exist_ok=True)
    if not os.path.exists(MINI_INDEX):
        print("[!] Error: mini_eval.index not found. Run Evaluation/mini_reindex.py first.")
        return

    shutil.copy(MINI_INDEX, os.path.join(FAISS_DIR_MINI, "mini_eval.index"))
    shutil.copy(MINI_IDS, os.path.join(FAISS_DIR_MINI, "mini_eval_ids.npy"))

    # 2. Swap Config
    print(f"[*] Switching config to use MINI index...")
    with open(CONFIG_PATH, "r") as f:
        original_config = f.read()

    mini_config = original_config.replace('FAISS_DIR', f'# FAISS_DIR') 
    mini_config += f'\nFAISS_DIR = r"{FAISS_DIR_MINI}"\n'

    try:
        with open(CONFIG_PATH, "w") as f:
            f.write(mini_config)

        # 3. Run Evaluation
        print(f"\n[*] STARTING EVALUATION (on 100 docs)...\n")
        # Use sys.executable to ensure we stay in the same VENV
        subprocess.run([sys.executable, "Evaluation/run_evals.py"], check=True)

    finally:
        # 4. Revert Config
        print(f"\n[*] REVERTING config to original index...")
        with open(CONFIG_PATH, "w") as f:
            f.write(original_config)
        
        print("\n[SUCCESS] Mini-Evaluation complete and system reverted.")

if __name__ == "__main__":
    main()
