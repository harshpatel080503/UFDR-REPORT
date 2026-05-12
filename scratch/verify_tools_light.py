import os
import sys
import json

# Add root to sys.path
ROOT_DIR = r"e:\Data Science Study\Deep Learning Project\UFDR"
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Mock RetrieverEngine for light test
import Reasoning.tool_executor
class MockRetriever:
    def search(self, query, k=10, use_reranker=True):
        return [{"page_id": "MOCK-1", "date": "2010-01-01", "user": "MOCK_USER", "action": "test", "text": "Mock search result"}], 0.1, 0.0

Reasoning.tool_executor.RetrieverEngine = MockRetriever

from Reasoning.tool_executor import ToolExecutor

def test_tools_light():
    executor = ToolExecutor()
    executor.retriever = MockRetriever()
    
    print("--- Testing GetPolicy ---")
    policy = executor.get_policy("USB_POLICY")
    print(policy)
    
    print("\n--- Testing CreateTicket ---")
    ticket = executor.create_ticket("Missing logs for Jan 2010", "Missing Data", "medium")
    print(ticket)
    
    print("\n--- Testing SearchKB (Sample Query) ---")
    search_results = executor.search_kb("USB activity")
    print(search_results)

if __name__ == "__main__":
    test_tools_light()
