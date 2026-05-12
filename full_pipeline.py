import sys
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Retriever"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reranker"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reasoning"))
sys.path.insert(0, os.path.join(ROOT_DIR, "CaseBuilder"))
sys.path.insert(0, os.path.join(ROOT_DIR, "GraphBuilder"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Reporter"))

from Retriever.engine import RetrieverEngine
from Reasoning.reasoner import ReasoningEngine
from CaseBuilder.case import CaseBuilder
from GraphBuilder.graph import GraphBuilder
from Reporter.report_gen import ReportGenerator
from session_manager import SessionManager
import chat_interface

BANNER = r"""
+----------------------------------------------------------------+
|                   UFDR Copilot -- Phase 1 Pipeline             |
+----------------------------------------------------------------+
|  Retrieve -> Rerank -> Reason -> Case -> Graph -> Report      |
+----------------------------------------------------------------+
"""

def main():
    if len(sys.argv) < 2:
        print(BANNER)
        print("Usage: python full_pipeline.py \"your query\"")
        return

    query = sys.argv[1]
    print(BANNER)
    print(f"[*] Starting full investigation for: '{query}'\n")

    print("[1/6] Initializing Forensic Engines ...")
    session = SessionManager()
    session.init_session(query.replace(" ", "_")[:20], query)
    
    retriever = RetrieverEngine()
    reasoner = ReasoningEngine() # Now uses gpt-oss:120b-cloud
    case_builder = CaseBuilder()
    graph_builder = GraphBuilder()
    reporter = ReportGenerator()

    print(f"\n[2/6] Retrieving & Reranking Evidence ...")
    results, t_search, t_rerank = retriever.search(query, k=50, use_reranker=True)
    
    if not results:
        print("  [!] No evidence found for this query.")
        return

    print(f"[3/6] Reasoning with GPT OSS 120b Cloud ...")
    analysis = reasoner.analyze(query, results[:20])
    print(f"  [+] Risk Score: {analysis.get('risk_score')}/10")
    print(f"  [+] Category: {analysis.get('threat_category')}")

    print(f"[4/6] Building Case Timelines ...")
    cases = case_builder.build_case(results)
    print(f"  [+] Identified {cases.get('subject_count')} subjects of interest.")

    print(f"[5/6] Constructing AI-Refined Knowledge Graph ...")
    
    ai_knowledge = reasoner.extract_graph_entities(results)
    
    graph_code = graph_builder.generate_graph(results, ai_knowledge=ai_knowledge)

    print(f"[6/6] Generating Final Investigation Report ...")
    
    narrative = reasoner.synthesize_report(query, analysis, cases, graph_code)
    
    report_path = reporter.generate(query, analysis, cases, graph_code, narrative=narrative)
    
    print("\n" + "="*60)
    print(f"COMPLETE: INVESTIGATION COMPLETE")
    print(f"Report Location: {os.path.abspath(report_path)}")
    print("="*60)

    # Save to session
    session.update_investigation(narrative, results, graph_code)
    
    print("\n[*] Handing off to UFDR Interactive Chat...")
    retriever.close()
    
    chat_interface.start_chat(os.path.basename(session.current_session_file))

if __name__ == "__main__":
    main()
