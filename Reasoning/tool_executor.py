import os
import json
import uuid
import sys
from typing import Dict, Any

# Ensure we can import from the root and all core components
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

for folder in ["Retriever", "CaseBuilder", "GraphBuilder", "Reporter", "Reasoning"]:
    comp_path = os.path.join(ROOT_DIR, folder)
    if comp_path not in sys.path:
        sys.path.insert(0, comp_path)

# Component Imports
from Retriever.engine import RetrieverEngine
from CaseBuilder.case import CaseBuilder
from GraphBuilder.graph import GraphBuilder
from Reporter.report_gen import ReportGenerator
from Reasoning.reasoner import ReasoningEngine

TICKETS_PATH = os.path.join(ROOT_DIR, "Copilot", "Data", "tickets.json")

class ToolExecutor:
    def __init__(self):
        # Tools initialized for the session
        self.retriever = RetrieverEngine()
        self.case_builder = CaseBuilder()
        self.graph_builder = GraphBuilder()
        self.reporter = ReportGenerator()
        self.reasoner = ReasoningEngine()

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Dispatcher for tool execution."""
        try:
            if tool_name == "CreateTicket":
                return self.create_ticket(arguments)
            elif tool_name == "SearchForensicLogs":
                # Kept for administrative use, but usually bypassed in strict chat mode
                return self.search_logs(arguments.get("query"), arguments.get("k", 10))
            else:
                return f"Error: Tool '{tool_name}' not available in this context."
        except Exception as e:
            return f"Error: {str(e)}"

    def create_ticket(self, args: Dict[str, Any]) -> str:
        """Formal escalation to human analysts for missing data."""
        import datetime
        ticket_id = f"UFDR-ESC-{uuid.uuid4().hex[:6].upper()}"
        ticket = {
            "ticket_id": ticket_id,
            "summary": args.get("summary"),
            "category": "Data Gap / Escalation",
            "severity": args.get("severity", "medium"),
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "OPEN",
            "notes": "Triggered by Copilot due to missing evidence in the generated report."
        }
        
        tickets = []
        if os.path.exists(TICKETS_PATH):
            with open(TICKETS_PATH, "r") as f:
                try: tickets = json.load(f)
                except: pass
        
        tickets.append(ticket)
        with open(TICKETS_PATH, "w") as f:
            json.dump(tickets, f, indent=2)
        
        return (
            f"STRICT ESCALATION SUCCESSFUL. Ticket ID: {ticket_id}. "
            "Since the information requested is not present in the current forensic report, "
            "it has been formally escalated for manual log retrieval."
        )

    def search_logs(self, query: str, k: int) -> str:
        # Limited internal search
        records, _, _ = self.retriever.search(query, k=min(k, 5), use_reranker=True)
        if not records: return "No additional logs found."
        lines = [f"[{r.get('date')}] {r.get('user')} | {r.get('text')[:100]}" for r in records]
        return "\n".join(lines)
