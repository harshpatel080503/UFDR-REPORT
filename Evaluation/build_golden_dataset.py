"""
Golden Dataset Builder for UFDR Evaluation (FAST VERSION)
----------------------------------------------------------
Uses OS-level findstr for fast grep through large JSONL files.
Builds 100 evaluation queries from CMU CERT r4.2 ground truth.
"""

import csv
import json
import os
import re
import subprocess
import random

random.seed(42)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSIDERS_CSV = os.path.join(BASE, "Data", "processed data",
                            "Insiders Ground Truth Labels", "insiders.csv")
PAGEINDEX_DIR = os.path.join(BASE, "Data", "processed data", "PageIndex_Data")
OUTPUT = os.path.join(os.path.dirname(__file__), "golden_dataset.json")

# Only scan small files (skip 8GB http.jsonl — use findstr for that)
SMALL_SOURCES = ["device.jsonl", "logon.jsonl", "file.jsonl"]
LARGE_SOURCES = ["http.jsonl", "email.jsonl"]

SCENARIO_META = {
    1: {"threat_category": "Data Exfiltration", "risk_score": 9,
        "description": "After-hours logon, removable drive, wikileaks.org uploads"},
    2: {"threat_category": "Insider Theft", "risk_score": 7,
        "description": "Job hunting on career sites, thumb-drive data theft before departure"},
    3: {"threat_category": "Sabotage", "risk_score": 10,
        "description": "Keylogger download, USB transfer to supervisor, impersonation email"},
}


def load_insiders():
    insiders = []
    with open(INSIDERS_CSV, "r") as f:
        for row in csv.DictReader(f):
            if row["dataset"] == "4.2":
                insiders.append({
                    "user": row["user"],
                    "scenario": int(row["scenario"]),
                    "start": row["start"],
                    "end": row["end"],
                })
    return insiders


def parse_date(d):
    for fmt in ("%m/%d/%Y %H:%M:%S", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            from datetime import datetime
            return datetime.strptime(d.strip(), fmt).strftime("%Y-%m-%d")
        except Exception:
            continue
    return None


def fast_grep_page_ids(user, max_ids=5):
    """Use findstr (Windows) for fast user lookup across all JSONL files."""
    ids = []
    for src in SMALL_SOURCES + LARGE_SOURCES:
        if len(ids) >= max_ids:
            break
        path = os.path.join(PAGEINDEX_DIR, src)
        if not os.path.exists(path):
            continue
        try:
            result = subprocess.run(
                ["findstr", "/C:" + user, path],
                capture_output=True, text=True, timeout=30,
                encoding="utf-8", errors="replace"
            )
            if result.returncode == 0 and result.stdout:
                for line in result.stdout.strip().split("\n")[:max_ids - len(ids)]:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        if rec.get("user") == user:
                            ids.append(rec["page_id"])
                    except Exception:
                        continue
        except subprocess.TimeoutExpired:
            continue
    return ids[:max_ids]


# ── Query Templates per Scenario ──────────────────────────────────────

S1_TEMPLATES = [
    ("Show all after-hours activity for user {user}",
     "User {user} logged in during non-business hours between {start} and {end} and accessed wikileaks.org using a removable drive, indicating {threat}."),
    ("Did {user} visit wikileaks.org?",
     "Evidence shows {user} visited wikileaks.org on multiple occasions while connected via USB device during {start}–{end}. This is a {threat} incident."),
    ("Find USB device connections by {user}",
     "User {user} connected removable devices between {start} and {end}, coinciding with visits to wikileaks.org and after-hours logon. High risk of {threat}."),
    ("Investigate data exfiltration by {user}",
     "Between {start} and {end}, {user} exhibited classic exfiltration: after-hours logon, USB connection, uploads to wikileaks.org."),
    ("List all wikileaks-related browsing for user {user}",
     "Multiple visits to wikileaks.org detected for {user} between {start} and {end}. Combined with USB and after-hours patterns, this is {threat}."),
    ("What suspicious web activity did {user} perform?",
     "During {start}–{end}, {user} visited wikileaks.org and connected USB devices after hours, strongly indicating data exfiltration."),
    ("Show logon anomalies for {user}",
     "User {user} showed anomalous after-hours logon patterns between {start} and {end}, coinciding with removable media use and wikileaks.org access."),
    ("Find evidence of insider threat for {user}",
     "User {user} is flagged as insider threat. Evidence: after-hours logons, USB connections, wikileaks.org visits between {start} and {end}."),
]

S2_TEMPLATES = [
    ("Show job hunting activity for user {user}",
     "User {user} browsed job websites (monster.com, careerbuilder.com, craigslist.org) between {start} and {end}, and escalated USB file transfers before departure."),
    ("Did {user} visit career websites before leaving?",
     "Evidence confirms {user} accessed career portals between {start} and {end}, including monster.com and careerbuilder.com, with increased thumb-drive usage."),
    ("Investigate thumb drive data theft by {user}",
     "Between {start} and {end}, {user} increased removable drive usage while browsing job-hunting sites, indicating pre-departure data theft."),
    ("Find file transfers and USB activity for {user}",
     "User {user} connected USB devices at elevated rates between {start} and {end}, correlating with career site browsing — suggesting data theft before resignation."),
    ("List all job-seeking web browsing by {user}",
     "During {start}–{end}, {user} visited monster.com, careerbuilder.com, and craigslist.org for job listings, combined with escalated USB file copies."),
    ("Show pre-resignation data exfiltration by {user}",
     "User {user} exhibited pre-resignation exfiltration: job-seeking from {start} to {end} with concurrent spikes in USB device connections."),
    ("Identify employees browsing competitor job portals",
     "User {user} visited lockheedmartin.com job postings and career portals between {start} and {end}, followed by USB data theft activity."),
    ("What data did {user} copy to removable media?",
     "Between {start} and {end}, {user} used thumb drives to copy files while actively job-hunting on career websites."),
]

S3_TEMPLATES = [
    ("Did {user} download a keylogger?",
     "User {user} downloaded keylogger software from refog.com and softactivity.com on {start}, then transferred the .exe via USB to a supervisor's machine."),
    ("Show keylogger-related activity for {user}",
     "On {start}, user {user} visited keylogger sites (refog.com, softactivity.com), downloaded an executable, and transferred it via USB device."),
    ("Investigate sabotage activity by {user}",
     "User {user} carried out sabotage between {start} and {end}: keylogger download, USB transfer to supervisor's PC, impersonation emails."),
    ("Find all malware download events for {user}",
     "Evidence shows {user} downloaded keylogger executables from refog.com on {start} and copied them to removable media for deployment."),
    ("Did any employee install unauthorized software?",
     "User {user} downloaded and deployed keylogger software between {start} and {end}. The .exe was transferred via USB to another workstation."),
    ("Show USB file copy events involving executables by {user}",
     "On {start}, {user} connected USB and copied a keylogger .exe, preceded by visits to keylogger vendor sites."),
    ("Find impersonation or credential theft by {user}",
     "Between {start} and {end}, {user} deployed a keylogger on supervisor's machine, harvested credentials, sent mass impersonation email."),
    ("List all security incidents involving {user}",
     "User {user} conducted multi-phase sabotage: keylogger download, USB deployment, credential harvest, impersonation email ({start}–{end})."),
]

GENERAL_TEMPLATES = [
    ("Show all security events involving user {user}",
     "Forensic logs show {user} was involved in {threat} activity ({desc}) between {start} and {end}."),
    ("List all USB connections by {user}",
     "USB device connections by {user} were recorded. This user is flagged for {threat} due to {desc}."),
    ("Which employees showed anomalous behavior between {start} and {end}?",
     "Anomalous behavior was detected for {user} during {start}–{end}, consistent with {threat} indicators."),
    ("Show forensic timeline for employee {user}",
     "Full forensic timeline for {user} ({start} to {end}) reveals {threat} patterns: {desc}."),
    ("What threat indicators exist for {user}?",
     "User {user} has multiple threat indicators: {desc}. Activity period: {start} to {end}. Classified as {threat}."),
    ("Summarize the investigation findings for {user}",
     "Investigation of {user} ({start}–{end}) concluded {threat}. Key evidence: {desc}."),
    ("Were there any data loss events between {start} and {end}?",
     "Data loss events detected for {user} during {start}–{end}: {desc}. Category: {threat}."),
    ("Show all removable media events on {start}",
     "Removable media events on {start} include activity by {user} flagged for {threat}."),
    ("Find all insider threat suspects in the organization",
     "User {user} is identified as a {threat} suspect based on {desc} from {start} to {end}."),
    ("What files did {user} access during the incident window?",
     "Between {start} and {end}, {user} accessed files consistent with {threat} behavior: {desc}."),
]


def build_entry(tq, ts, insider, meta, page_ids, qid):
    start = parse_date(insider["start"]) or "2010-06-01"
    end = parse_date(insider["end"]) or "2010-06-30"
    user = insider["user"]
    threat = meta["threat_category"]
    desc = meta["description"]

    query = tq.format(user=user, start=start, end=end, threat=threat, desc=desc)
    summary = ts.format(user=user, start=start, end=end, threat=threat, desc=desc)
    return {
        "query_id": f"Q{qid:03d}",
        "query": query,
        "expected_log_ids": page_ids,
        "expected_threat_category": threat,
        "expected_risk_score": meta["risk_score"],
        "ideal_summary": summary,
        "scenario": insider["scenario"],
        "insider_user": user,
    }


def main():
    print("[*] Loading insider ground truth from insiders.csv...")
    insiders = load_insiders()

    by_scenario = {1: [], 2: [], 3: []}
    for ins in insiders:
        if ins["scenario"] in by_scenario:
            by_scenario[ins["scenario"]].append(ins)

    for s, lst in by_scenario.items():
        print(f"    Scenario {s}: {len(lst)} insiders")

    templates_map = {1: S1_TEMPLATES, 2: S2_TEMPLATES, 3: S3_TEMPLATES}
    dataset = []
    qid = 1

    # Phase 1: Scenario-specific queries (~30 each = ~70 from S1+S2+S3)
    # S1 has 30 users, S2 has 30, S3 has 10 → 70 scenario queries
    print("\n[*] Phase 1: Building scenario-specific queries...")
    for scenario_id in [1, 2, 3]:
        meta = SCENARIO_META[scenario_id]
        templates = templates_map[scenario_id]

        for i, insider in enumerate(by_scenario[scenario_id]):
            user = insider["user"]
            print(f"    [{qid:03d}] S{scenario_id} | {user} — fast grep...", end="")
            page_ids = fast_grep_page_ids(user, max_ids=5)
            print(f" found {len(page_ids)} ids")

            tq, ts = templates[i % len(templates)]
            dataset.append(build_entry(tq, ts, insider, meta, page_ids, qid))
            qid += 1

    # Phase 2: General / cross-scenario queries to reach 100
    remaining = 100 - len(dataset)
    print(f"\n[*] Phase 2: Building {remaining} general queries...")
    all_insiders = insiders.copy()
    random.shuffle(all_insiders)

    for i in range(remaining):
        insider = all_insiders[i % len(all_insiders)]
        meta = SCENARIO_META[insider["scenario"]]
        tq, ts = GENERAL_TEMPLATES[i % len(GENERAL_TEMPLATES)]
        user = insider["user"]
        print(f"    [{qid:03d}] General | {user}...", end="")
        page_ids = fast_grep_page_ids(user, max_ids=5)
        print(f" found {len(page_ids)} ids")
        dataset.append(build_entry(tq, ts, insider, meta, page_ids, qid))
        qid += 1

    # Save
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"  GOLDEN DATASET COMPLETE")
    print(f"  Total queries : {len(dataset)}")
    print(f"  Output        : {OUTPUT}")
    s_counts = {}
    for e in dataset:
        s_counts[e.get("scenario", "?")] = s_counts.get(e.get("scenario", "?"), 0) + 1
    for s, c in sorted(s_counts.items()):
        print(f"  Scenario {s}    : {c} queries")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
