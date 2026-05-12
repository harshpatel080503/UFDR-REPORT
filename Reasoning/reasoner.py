import requests
import json
import time
import os

class ReasoningEngine:
    def __init__(self, model="gpt-oss:120b-cloud", base_url=None):
        self.model = model
        self.api_key = os.getenv("OLLAMA_API_KEY")
        default_url = "https://ollama.com" if self.api_key else "http://localhost:11434"
        self.base_url = base_url or os.getenv("OLLAMA_CLOUD_URL", default_url)
        self.url = f"{self.base_url.rstrip('/')}/api/chat"
        self.headers = {}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
            
        self.system_prompt = (
            "You are a Senior Digital Forensics Investigator. Your task is to analyze a set of "
            "retrieved evidence and provide a clear, professional security assessment. "
            "STRICT GROUNDING: You MUST ONLY use the technical details present in the provided evidence. "
            "Categorize into: ['Data Exfiltration', 'Insider Theft', 'Sabotage', 'None']. "
            "Assign a Risk Score (0-10)."
        )

    def analyze(self, query, evidence):
        if not evidence:
            return {"risk_score": 0, "summary": "No evidence.", "threat_category": "None"}
        evidence_text = ""
        for i, rec in enumerate(evidence, 1):
            evidence_text += f"\n[{i}] {rec['date']} | {rec['user']} | {rec['action']} | {rec['text']}"
        prompt = (
            f"USER QUERY: {query}\n"
            f"RETRIEVED EVIDENCE:{evidence_text}\n\n"
            "Analyze the above evidence and output a JSON object with: threat_category, risk_score, summary, key_findings."
        )
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}],
            "stream": False, "format": "json"
        }
        try:
            response = requests.post(self.url, json=payload, headers=self.headers, timeout=300)
            response.raise_for_status()
            res_json = response.json()
            return json.loads(res_json['message']['content'])
        except Exception as e:
            return {"risk_score": 0, "summary": f"Error: {e}", "threat_category": "None"}

    def _call_llm_narrative(self, system_prompt, user_prompt, timeout=600):
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            "stream": False
        }
        try:
            response = requests.post(self.url, json=payload, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            return response.json()['message']['content']
        except Exception as e:
            return f"\n[ERROR] {e}\n"

    def synthesize_report(self, query, analysis, cases, graph_code):
        print(f"    [-->] Starting COMPREHENSIVE Multi-Pass Forensic Synthesis...")

        print("      [1/3] Section 1-4: Executive Summary & Detailed Subject Profiles...")
        p1_prompt = (
            "Create Sections 1-4 of a DETAILED investigative report.\n"
            "Include: 1. EXECUTIVE SUMMARY (min 500 words, deep context), 2. PRELIMINARY CASE INFO, 3. INCIDENT SUMMARY (Full story), 4. ALLEGATION SUBJECTS (Full profile for EVERY user in the 'CASES' data).\n"
            f"QUERY: {query}\nANALYSIS: {json.dumps(analysis)}\nCASES: {json.dumps(cases)}\n"
            "MANDATORY: Clearly list all suspects and their involvement. DO NOT summarize. Be exhaustive. OUTPUT MARKDOWN ONLY."
        )
        stage1 = self._call_llm_narrative("You are a Lead Investigator. Write the initial report foundation.", p1_prompt)

        print("      [2/3] Section 5-8: Diaries & Virtual Interviews...")
        p2_prompt = (
            "Create Sections 5-8.\n"
            "Include: 5. INVESTIGATION DETAILS (Minute-by-minute timeline), 6. INVESTIGATION INTERVIEWS (Deep transcripts for ALL suspects), 7. CREDIBILITY ASSESSMENT (Clinical evaluation), 8. EVIDENCE COLLECTION (Deep technical analysis).\n"
            f"FORENSIC DATA: {json.dumps(analysis)}\n"
            f"CASES DATA: {json.dumps(cases)}\n"
            "STRICT GROUNDING: Narrative depth based on actual logs. OUTPUT MARKDOWN ONLY."
        )
        stage2 = self._call_llm_narrative("You are a Lead Investigator. Author the evidence and interview chapters.", p2_prompt)

        print("      [3/3] Section 9-10: Verdict & Enterprise Mapping...")
        p3_prompt = (
            "Create Sections 9-10.\n"
            "Include: 9. CONCLUSION & RECOMMENDATIONS (Definitive ruling for ALL subjects), 10. FINAL REVIEW & APPENDICES (Mermaid graph + Evidence source table).\n"
            f"GRAPH CODE:\n{graph_code}\n"
            f"ANALYSIS: {json.dumps(analysis)}\n"
            "MANDATORY: A definitive institutional conclusion for the entire scope. OUTPUT MARKDOWN ONLY."
        )
        stage3 = self._call_llm_narrative("You are a Lead Investigator. Finalize the investigation.", p3_prompt)

        return f"{stage1}\n\n{stage2}\n\n{stage3}"

    def extract_graph_entities(self, evidence):
        # (Keeping the original logic but simplified for brevity in this scratch rewrite if needed)
        # For now, I'll just use the original logic from the file I viewed.
        evidence_text = ""
        for i, rec in enumerate(evidence[:10], 1):
            evidence_text += f"\n[{i}] {rec['user']} | {rec['action']} | {rec['text']}"
        prompt = (
            "Extract a KNOWLEDGE GRAPH mapping (JSON).\n"
            f"EVIDENCE:\n{evidence_text}\n"
            "JSON structure: {\"entities\": [...], \"relationships\": [...]}"
        )
        payload = {
            "model": self.model, "messages": [{"role": "user", "content": prompt}], "stream": False, "format": "json"
        }
        try:
            response = requests.post(self.url, json=payload, headers=self.headers, timeout=300)
            return json.loads(response.json()['message']['content'])
        except:
            return {"entities": [], "relationships": []}
