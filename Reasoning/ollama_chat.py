import os
import requests
import json
import time
from typing import List, Dict

try:
    from tools import get_tools_schema
    from tool_executor import ToolExecutor
except ImportError:
    from Reasoning.tools import get_tools_schema
    from Reasoning.tool_executor import ToolExecutor

class GPTOSS120BChatEngine:
    def __init__(self, model_name="gpt-oss:120b-cloud", api_key=None):
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")
        default_url = "https://ollama.com" if self.api_key else "http://localhost:11434"
        base_url = os.getenv("OLLAMA_CLOUD_URL", default_url)
        self.url = f"{base_url.rstrip('/')}/api/chat"
        self.model_name = model_name
        self.chat_history = []
        self.report_context = ""
        self.log_context = ""
        self.tool_executor = ToolExecutor()
        self.tools = get_tools_schema()

    def set_system_context(self, report: str, evidence: List[Dict]):
        self.report_context = report
        log_entries = []
        for e in evidence[:20]:
            log_entries.append(f"[{e.get('date')}] {e.get('user')} | {e.get('action')} | {e.get('text')}")
        self.log_context = "\n".join(log_entries)

    def get_response(self, user_query: str) -> str:
        system_instruction = (
            "You are the UFDR Copilot, a strict forensic assistant. Your intelligence is DERIVED ONLY from the provided report and logs.\n"
            "STRICT CITATION POLICY:\n"
            "1. MANDATORY BRACKETS: You MUST use standard square brackets [ ] for all citations.\n"
            "2. FORMAT: Use [doc_id: <id>] for logs or [Report: Section Name] for report content.\n"
            "3. NO OTHER SYMBOLS: Do NOT use 【 】 or <cite>. Only use [ ].\n"
            "4. POSITIONING: Place the citation [ ] immediately after the fact it supports.\n"
            "5. NO TABLES: Use bold headings and bullet points only.\n"
            "6. IF NOT IN REPORT: Call 'CreateTicket' immediately. Do not speculate.\n\n"
            f"--- FORENSIC REPORT ---\n{self.report_context}\n\n"
            f"--- INITIAL LOGS ---\n{self.log_context}"
        )

        messages = [{"role": "system", "content": system_instruction}]
        for msg in self.chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_query})
        
        for _ in range(2):
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "tools": self.tools,
                "options": {"num_predict": 1024, "temperature": 0.0}
            }

            headers = {"Content-Type": "application/json"}
            if self.api_key: headers["Authorization"] = f"Bearer {self.api_key}"
            
            try:
                response = requests.post(self.url, headers=headers, data=json.dumps(payload), timeout=180)
                response.raise_for_status()
                res_json = response.json()
                
                message = res_json['message']
                content = message.get('content', "")
                tool_calls = message.get('tool_calls', [])

                if not tool_calls:
                    self.chat_history.append({"role": "user", "content": user_query})
                    self.chat_history.append({"role": "assistant", "content": content})
                    return content

                messages.append(message)
                for tool_call in tool_calls:
                    func_name = tool_call['function']['name']
                    args = tool_call['function']['arguments']
                    print(f"  [!] Missing Data Detected. Escalating via {func_name}...")
                    tool_result = self.tool_executor.execute(func_name, args)
                    messages.append({"role": "tool", "content": tool_result, "name": func_name})
                
            except Exception as e:
                return f"Forensic Sync Error: {str(e)}"
        
        return "Error: Maximum grounding depth reached."

    def reset_history(self, new_history: List[Dict] = None):
        self.chat_history = new_history or []
