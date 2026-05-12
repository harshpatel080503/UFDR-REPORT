import os
import sys
from dotenv import load_dotenv

# Adjust paths
ROOT_DIR = r"e:\Data Science Study\Deep Learning Project\UFDR"
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Reasoning"))

load_dotenv(os.path.join(ROOT_DIR, ".env"))

from Reasoning.reasoner import ReasoningEngine

def test_connection():
    print(f"OLLAMA_API_KEY: {os.getenv('OLLAMA_API_KEY')[:10]}...")
    print(f"OLLAMA_CLOUD_URL: {os.getenv('OLLAMA_CLOUD_URL')}")
    
    reasoner = ReasoningEngine()
    print(f"Reasoner URL: {reasoner.url}")
    
    # Simple query
    evidence = [{"date": "2010-06-28", "user": "test", "text": "test logon", "action": "login"}]
    analysis = reasoner.analyze("Is there any risk?", evidence)
    print(f"Analysis: {analysis.get('threat_category')}")

if __name__ == "__main__":
    test_connection()
