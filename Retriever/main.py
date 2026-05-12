import sys
import os
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import RetrieverEngine
from retriever_config import RETRIEVER_K, TEXT_WRAP_WIDTH

BANNER = r"""
    +---------------------------------------------------+
    |        UFDR Copilot -- Semantic Retriever          |
    +---------------------------------------------------+
    |  Searching 12.5M records across 7 FAISS shards    |
    |  Model: all-MiniLM-L6-v2  |  Store: SQLite        |
    +---------------------------------------------------+
"""

def print_result(i, rec):
    """Format and print a single retrieval result."""
    shard   = rec["_shard"]
    score   = rec["_search_score"]
    rerank  = rec.get("_rerank_score")
    user    = rec["user"]
    action  = rec["action"]
    date    = rec["date"]
    full_txt = rec.get("text", "")
    
    wrapped = textwrap.wrap(full_txt, width=TEXT_WRAP_WIDTH)
    
    score_str = f"FAISS: {score:.4f}"
    if rerank is not None:
        score_str += f" | Rerank: {rerank:.4f}"
        
    header = f" {i}. [{shard}]  {score_str}  |  {date}  |  {user}  |  {action}"
    print(f"\n{header}")
    print("─" * len(header))
    for line in wrapped:
        print(f"   {line}")

def main():
    print(BANNER)
    
    try:
        engine = RetrieverEngine()
    except Exception as e:
        print(f"\n  Failed to initialize engine: {e}")
        return

    rerank_active = True
    print(f"\n  [+] Retriever ready. Reranking: {'ON' if rerank_active else 'OFF'}")
    print("      (Type '/rerank' to toggle, 'exit' to quit)")
    
    while True:
        try:
            query = input(f"\n[Search Query] {'(Reranked)' if rerank_active else ''} > ").strip()
            
            if not query:
                continue
            if query.lower() in ("exit", "quit", "q"):
                break
            
            if query.lower() == "/rerank":
                rerank_active = not rerank_active
                print(f"  [!] Reranking is now {'ON' if rerank_active else 'OFF'}")
                continue
                
            print(f"  Searching ...")
            results, elapsed, r_dt = engine.search(query, k=RETRIEVER_K, use_reranker=rerank_active)
            
            if not results:
                print("  [!] No relevant results found.")
                continue
                
            msg = f"  Found {len(results)} results in {elapsed:.3f}s"
            if r_dt > 0:
                msg += f" (Rerank: {r_dt:.3f}s)"
            print(msg)
            print("═" * 100)
            
            for i, rec in enumerate(results, 1):
                print_result(i, rec)
                
            print(f"\n" + "═" * 100)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n  Search error: {e}")

    print("\n  Closing connections ...")
    engine.close()
    print("  Goodbye!")

if __name__ == "__main__":
    main()
