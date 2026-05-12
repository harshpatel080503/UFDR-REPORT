import os
import sys
import json

# Add root to sys.path
ROOT_DIR = r"e:\Data Science Study\Deep Learning Project\UFDR"
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from Reasoning.tool_executor import ToolExecutor

def test_tools():
    executor = ToolExecutor()
    
    print("--- Testing GetPolicy ---")
    policy = executor.get_policy("USB_POLICY")
    print(policy)
    
    print("\n--- Testing CreateTicket ---")
    ticket = executor.create_ticket("Missing logs for Jan 2010", "Missing Data", "medium")
    print(ticket)
    
    print("\n--- Testing SearchKB (Sample Query) ---")
    # This requires the retriever to be working and indexes to exist
    try:
        search_results = executor.search_kb("USB activity for user CSC0217")
        print(search_results[:500] + "..." if len(search_results) > 500 else search_results)
    except Exception as e:
        print(f"SearchKB failed (expected if indexes not loaded): {e}")

if __name__ == "__main__":
    test_tools()
