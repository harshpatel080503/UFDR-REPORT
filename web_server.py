import os
import sys
import json
import uuid
import datetime
import asyncio
import multiprocess
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict

# Windows Multiprocessing Patch
if sys.platform == 'win32':
    import multiprocess.resource_tracker
    def remove_shm_from_resource_tracker():
        try: multiprocess.resource_tracker._resource_tracker._stop()
        except: pass

# Root path alignment
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

for folder in ["Retriever", "CaseBuilder", "GraphBuilder", "Reporter", "Reasoning"]:
    comp_path = os.path.join(ROOT_DIR, folder)
    if comp_path not in sys.path: sys.path.insert(0, comp_path)

from Retriever.engine import RetrieverEngine
from Reasoning.reasoner import ReasoningEngine
from CaseBuilder.case import CaseBuilder
from GraphBuilder.graph import GraphBuilder
from Reporter.report_gen import ReportGenerator
from Reasoning.ollama_chat import GPTOSS120BChatEngine
from session_manager import SessionManager

app = FastAPI(title="UFDR Forensic Command Center API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Engines
print("[*] UFDR ENGINE: Initializing Dashboard Systems...")
retriever = RetrieverEngine()
reasoner = ReasoningEngine()
case_builder = CaseBuilder()
graph_builder = GraphBuilder()
reporter = ReportGenerator()
chat_engine = GPTOSS120BChatEngine()

# Global Thread Pool for parallelizing forensic stages
executor = ThreadPoolExecutor(max_workers=4)
STATUS_FILE = "investigation_status.json"

def update_status(session_id: str, status_data: dict):
    try:
        current_status = {}
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r") as f: current_status = json.load(f)
        current_status[session_id] = status_data
        with open(STATUS_FILE, "w") as f: json.dump(current_status, f)
    except: pass

async def run_forensic_pipeline_task(session_id: str, query: str):
    try:
        loop = asyncio.get_event_loop()
        session = SessionManager()
        session.current_session_file = os.path.join(session.sessions_dir, session_id)
        session.state["case_id"] = session_id.replace('.json', '')
        session.state["query"] = query
        session.save()
        
        # 1. High-Speed Evidence Retrieval
        update_status(session_id, {"status": "searching", "progress": 15, "message": "Parallel Shard Retrieval..."})
        results, _, _ = retriever.search(query, k=40, use_reranker=True) # Optimized K for speed
        
        if not results:
            update_status(session_id, {"status": "failed", "message": "No evidence shards found."})
            return

        # 2. Parallel Processing Phase (Analysis + Case Building + Graph Prep)
        update_status(session_id, {"status": "processing", "progress": 50, "message": "Executing Parallel Forensic Tasks..."})
        
        # Run independent tasks in parallel using thread pool
        analysis_task = loop.run_in_executor(executor, reasoner.analyze, query, results[:15])
        case_task = loop.run_in_executor(executor, case_builder.build_case, results)
        knowledge_task = loop.run_in_executor(executor, reasoner.extract_graph_entities, results[:10])
        
        # Wait for all parallel tasks to complete
        analysis, cases, ai_knowledge = await asyncio.gather(analysis_task, case_task, knowledge_task)
        
        # 3. Final Topology Mapping
        update_status(session_id, {"status": "mapping", "progress": 75, "message": "Mapping Cyber Surface..."})
        graph_code = graph_builder.generate_graph(results[:15], ai_knowledge=ai_knowledge)
        
        # 4. Narrative Synthesis
        update_status(session_id, {"status": "synthesizing", "progress": 90, "message": "Synthesizing Final Verdict..."})
        narrative = reasoner.synthesize_report(query, analysis, cases, graph_code)
        
        session.update_investigation(narrative, results, graph_code)
        session.save()
        
        update_status(session_id, {"status": "complete", "progress": 100, "message": "Investigation Finished."})
    except Exception as e:
        print(f"[CRITICAL ERROR] Pipeline Failure: {str(e)}")
        update_status(session_id, {"status": "failed", "message": str(e)})

class InvestigationRequest(BaseModel):
    query: str

class RenameRequest(BaseModel):
    new_query: str

@app.post("/api/investigate")
async def investigate(req: InvestigationRequest, background_tasks: BackgroundTasks):
    case_slug = req.query.replace(' ', '_')[:20]
    session_id = f"{case_slug}_{int(datetime.datetime.now().timestamp())}.json"
    update_status(session_id, {"status": "queued", "progress": 5, "message": "Queueing Engines..."})
    background_tasks.add_task(run_forensic_pipeline_task, session_id, req.query)
    return {"status": "started", "session_id": session_id}

@app.get("/api/status/{session_id}")
async def get_status(session_id: str):
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f: return json.load(f).get(session_id, {"status": "pending"})
    return {"status": "pending"}

@app.get("/api/sessions")
async def list_sessions():
    session_mgr = SessionManager()
    sessions_dir = session_mgr.sessions_dir
    if not os.path.exists(sessions_dir): return []
    files = [f for f in os.listdir(sessions_dir) if f.endswith('.json')]
    sessions_list = []
    for f in files:
        try:
            with open(os.path.join(sessions_dir, f), "r") as s:
                data = json.load(s)
                display_name = data.get("query") or f.replace('.json', '').replace('_', ' ')
                sessions_list.append({"id": f, "query": display_name})
        except: continue
    return sorted(sessions_list, key=lambda x: x['id'], reverse=True)

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    session_mgr = SessionManager()
    if not session_mgr.load(session_id): raise HTTPException(status_code=404)
    return session_mgr.state

@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    session_mgr = SessionManager()
    path = os.path.join(session_mgr.sessions_dir, session_id)
    if os.path.exists(path):
        os.remove(path)
        return {"status": "deleted"}
    raise HTTPException(status_code=404)

@app.patch("/api/session/{session_id}")
async def rename_session(session_id: str, req: RenameRequest):
    session_mgr = SessionManager()
    if session_mgr.load(session_id):
        session_mgr.state["query"] = req.new_query
        session_mgr.save()
        return {"status": "renamed"}
    raise HTTPException(status_code=404)

@app.post("/api/chat")
async def chat(req: dict):
    session = SessionManager()
    if not session.load(req["session_id"]): raise HTTPException(status_code=404)
    chat_engine.set_system_context(session.state["report"], session.state["evidence_set"])
    chat_engine.reset_history(session.state["chat_history"])
    response = chat_engine.get_response(req["message"])
    session.add_chat_message("user", req["message"])
    session.add_chat_message("assistant", response)
    session.save()
    return {"response": response}

@app.get("/api/tickets")
async def get_tickets():
    path = os.path.join(ROOT_DIR, "Copilot", "Data", "tickets.json")
    if os.path.exists(path):
        with open(path, "r") as f: return json.load(f)
    return []

dist_path = os.path.join(ROOT_DIR, "ufdr-web-app", "dist")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
