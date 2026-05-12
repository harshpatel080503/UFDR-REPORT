import sys
import os

# Add the project root to sys.path
sys.path.append(r"e:\Data Science Study\Deep Learning Project\UFDR")
sys.path.append(r"e:\Data Science Study\Deep Learning Project\UFDR\Retriever")

from Retriever.engine import RetrieverEngine

engine = RetrieverEngine()
query = "Show all after-hours activity for user AAM0658"
results, elapsed, _ = engine.search(query, k=10)

print(f"Query: {query}")
print(f"Elapsed: {elapsed:.4f}s")
print(f"Results (top 10):")
for i, r in enumerate(results):
    print(f"{i+1}. {r.get('page_id')} (Score: {r.get('_search_score'):.4f}) - {r.get('text')[:100]}...")

expected_ids = ["logon_001403", "logon_002778", "logon_003973", "logon_005388", "logon_006521"]
print(f"\nExpected IDs: {expected_ids}")
found = [rid for rid in [r.get('page_id') for r in results] if rid in expected_ids]
print(f"Found IDs in top 10: {found}")
