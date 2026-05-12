import json
import os
import time
from datetime import datetime

class SessionManager:
    def __init__(self, sessions_dir="sessions"):
        self.sessions_dir = sessions_dir
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
        
        self.current_session_file = None
        self.state = {
            "case_id": "",
            "query": "",
            "report": "",
            "evidence_set": [],
            "graph_code": "",
            "chat_history": [],
            "snapshots": []
        }

    def init_session(self, case_id, query):
        self.state["case_id"] = case_id
        self.state["query"] = query
        filename = f"{case_id}_{int(time.time())}.json"
        self.current_session_file = os.path.join(self.sessions_dir, filename)
        self.save()

    def update_investigation(self, report, evidence_set, graph_code):
        self.state["report"] = report
        self.state["evidence_set"] = evidence_set
        self.state["graph_code"] = graph_code
        self.create_snapshot("Investigation Complete")
        self.save()

    def add_chat_message(self, role, content):
        self.state["chat_history"].append({"role": role, "content": content})
        self.save()

    def create_snapshot(self, description):
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "chat_history_len": len(self.state["chat_history"]),
            # We store a shallow copy of the state at this point
            "chat_history_snapshot": list(self.state["chat_history"])
        }
        self.state["snapshots"].append(snapshot)

    def rewind(self, snapshot_index):
        """
        Time Travel: Revert to a specific snapshot index.
        """
        if 0 <= snapshot_index < len(self.state["snapshots"]):
            snapshot = self.state["snapshots"][snapshot_index]
            self.state["chat_history"] = list(snapshot["chat_history_snapshot"])
            # Remove snapshots ahead of this one
            self.state["snapshots"] = self.state["snapshots"][:snapshot_index + 1]
            self.save()
            return True
        return False

    def save(self):
        if self.current_session_file:
            with open(self.current_session_file, "w") as f:
                json.dump(self.state, f, indent=4)

    def load(self, filename):
        filepath = os.path.join(self.sessions_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.state = json.load(f)
            self.current_session_file = filepath
            return True
        return False

    def list_sessions(self):
        return [f for f in os.listdir(self.sessions_dir) if f.endswith(".json")]
