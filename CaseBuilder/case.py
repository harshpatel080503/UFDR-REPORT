from collections import defaultdict

class CaseBuilder:
    def __init__(self):
        self.severity_map = {
            "file_copy": 10,
            "file_delete": 9,
            "removable_media": 9,
            "reg_modify": 8,
            "process_start": 7,
            "login": 5,
            "visit_url": 3,
            "file_access": 4
        }

    def build_case(self, evidence):
        if not evidence:
            return {"cases": []}

        users_map = defaultdict(list)
        for rec in evidence:
            user = rec.get("user", "Unknown")
            users_map[user].append(rec)

        cases = []
        for user, events in users_map.items():
            sorted_events = sorted(events, key=lambda x: str(x.get("date", "")))
            best_action = "activity"
            max_sev = -1
            
            for e in sorted_events:
                action = e.get("action", "").lower()
                sev = self.severity_map.get(action, 1)
                if sev > max_sev:
                    max_sev = sev
                    best_action = action

            sources = [e.get("_shard", "unknown") for e in sorted_events]
            source_summary = {s: sources.count(s) for s in set(sources)}

            case = {
                "user_id": user,
                "event_count": len(events),
                "primary_action": best_action,
                "max_severity": max_sev,
                "sources": source_summary,
                "start_date": sorted_events[0].get("date"),
                "end_date": sorted_events[-1].get("date"),
                "timeline": sorted_events
            }
            cases.append(case)
        cases.sort(key=lambda x: (x["max_severity"], x["event_count"]), reverse=True)

        return {
            "cases": cases,
            "subject_count": len(cases),
            "total_evidence": len(evidence)
        }

if __name__ == "__main__":
    builder = CaseBuilder()
    test_data = [
        {"user": "USER1", "date": "2010-01-01", "action": "login"},
        {"user": "USER1", "date": "2010-01-02", "action": "file_copy"},
        {"user": "USER2", "date": "2010-01-01", "action": "visit_url"}
    ]
    result = builder.build_case(test_data)
    print(f"Subjects: {result['subject_count']}")
    for c in result['cases']:
        print(f"  User: {c['user_id']} | Events: {c['event_count']}")
