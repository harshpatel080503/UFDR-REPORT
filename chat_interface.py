import sys
import os
import time
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from session_manager import SessionManager

# Fixing import path logic
sys.path.append(os.path.join(os.path.dirname(__file__), "Reasoning"))
from ollama_chat import GPTOSS120BChatEngine

BANNER = r"""
+-------------------------------------------------------+
|             UFDR Interactive Forensic Chat            |
+-------------------------------------------------------+
|  Commands:                                            |
|  - 'rewind' : Go back in time                         |
|  - 'report' : Show investigation report               |
|  - 'exit'   : Save and exit                           |
+-------------------------------------------------------+
"""

def typewriter_print(text, speed=0.01):
    """Prints text with a typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        # Randomized delay to make it feel more human
        time.sleep(speed * random.uniform(0.5, 1.5))
    print()

def start_chat(session_file=None):
    session = SessionManager()
    
    if session_file:
        if not session.load(session_file):
            print(f"[!] Could not load session {session_file}")
            return
    else:
        sessions = session.list_sessions()
        if sessions:
             def get_timestamp(f):
                try:
                    return int(f.split("_")[-1].split(".")[0])
                except:
                    return 0
             sessions.sort(key=get_timestamp)
             session_file = sessions[-1]
             session.load(session_file)
        else:
            print("[!] No active session found. Please run the investigation first.")
            return

    print("\n[*] Initializing UFDR Copilot Ecosystem...")
    chat_engine = GPTOSS120BChatEngine()
    chat_engine.set_system_context(session.state["report"], session.state["evidence_set"])
    chat_engine.reset_history(session.state["chat_history"])

    print(BANNER)
    print(f"[*] Connected to {chat_engine.model_name}")
    print("[*] Ready for forensic queries. (Low-Latency Mode: Enabled)")

    while True:
        try:
            user_input = input("\n[Investigator] > ").strip()
            
            if user_input.lower() in ["exit", "bye", "quit"]:
                print("[*] Saving session and exiting...")
                session.save()
                break
            
            if user_input.lower() == "report":
                print("\n--- FORENSIC REPORT ---")
                typewriter_print(session.state["report"], speed=0.005)
                print("-----------------------\n")
                continue
                
            if user_input.lower() == "rewind":
                print("\n[?] Available Snapshots:")
                for i, s in enumerate(session.state["snapshots"]):
                    print(f"  [{i}] {s['timestamp']} - {s['description']}")
                
                idx = input("\n[Select Index to Rewind to] > ")
                if idx.isdigit() and session.rewind(int(idx)):
                    print(f"[*] Time Travel Successful. Reverted to Snapshot {idx}.")
                    chat_engine.reset_history(session.state["chat_history"])
                else:
                    print("[!] Invalid index.")
                continue

            if not user_input:
                continue

            # Get response from GPT-OSS-120B
            print("[*] Copilot is investigating...")
            response = chat_engine.get_response(user_input)
            
            # Sanitize response for Windows console
            safe_response = response.replace("\u202f", " ").replace("\u2011", "-")
            
            print(f"\n[UFDR Copilot]")
            typewriter_print(safe_response, speed=0.01)
            
            # Sync session history
            session.state["chat_history"] = chat_engine.chat_history
            session.save()

        except KeyboardInterrupt:
            print("\n[*] Exiting...")
            session.save()
            break

if __name__ == "__main__":
    start_chat()
