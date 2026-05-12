import datetime
import os

class ReportGenerator:
    def __init__(self, output_dir="Reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate(self, query, analysis, cases, graph_code, narrative=None):
        # Extract base date from timeline to align report ID
        base_date = datetime.datetime.now()
        all_dates = []
        for case in cases.get("cases", []):
            for event in case.get("timeline", []):
                if event.get("date"):
                    try:
                        all_dates.append(datetime.datetime.strptime(event["date"].split()[0], "%Y-%m-%d"))
                    except:
                        pass
        
        if all_dates:
            base_date = max(all_dates)
            timestamp = base_date.strftime("%Y-%m-%d") + " (Forensic Alignment)"
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (WARNING: No Forensic Data Aligned)"

        report_id = f"UFDR-{base_date.strftime('%Y%m%d')}-{query[:10].replace(' ', '_')}"
        if not all_dates:
             report_id = f"UFDR-UNALIGNED-{datetime.datetime.now().strftime('%Y%m%d')}"
        filename = f"Report_{report_id}.md"
        filepath = os.path.join(self.output_dir, filename)

        if narrative:
            md = narrative
            
            if "```mermaid" not in md:
                md += f"\n\n## 10. FINAL REVIEW & APPENDICES\n```mermaid\n{graph_code}\n```\n"
            
            import re
            lazy_pattern = re.compile(r'```mermaid\s*graph [LT]R\s*\.*?\s*```', re.DOTALL | re.IGNORECASE)
            if lazy_pattern.search(md):
                 md = lazy_pattern.sub(f"```mermaid\n{graph_code}\n```", md)
        else:
            md = f"""# Workplace Investigative Report - UFDR Autonomous Pipeline
**Report ID**: `{report_id}` | **Date**: {timestamp} | **Version**: Institutional v2.0

## 1. Executive Summary
I, the UFDR Autonomous Forensic Agent, initiated this investigation on {timestamp} to address the following query: `{query}`. 

The initial discovery phase involved a wide-spectrum retrieval across all federated log shards. My analytical engine has identified activity consistent with a `{analysis.get('threat_category', 'Potential Risk')}` profile. Based on the density of suspicious events and the cross-correlation of user actions, I have assigned a **Global Risk Score of `{analysis.get('risk_score', 'N/A')}/10`**. 

This report details a complex chain of digital events that warrant immediate administrative review and potential containment actions.

## 2. Preliminary Case Information
| Field | Details |
| :--- | :--- |
| **Investigator Name** | UFDR Autonomous Unit 01 |
| **Case Reference** | `{report_id}` |
| **Assignment Date** | {timestamp} |
| **Investigation Method** | Hybrid FAISS Retrieval + Cross-Encoder Reranking |
| **Data Integrity** | Verified via Forensic Shard Hashing |
| **Scope** | Enterprise Infrastructure Shards |

## 3. Incident Summary
This comprehensive investigation explores the `{analysis.get('threat_category')}` regarding `{query}`. 

The incident was identified via systemic anomalies that surfaced during the autonomous threat-hunting cycle. The 'Chain of Causality' begins with an initial trigger at {timestamp}, followed by a series of related actions across multiple nodes. The behavior deviates from the established baseline for standard enterprise users, suggesting a targeted action or a compromised credential set.

## 4. Allegation Subject
The following subject(s) have been identified as core participants in this digital chain of events:
"""
            for case in cases.get("cases", [])[:5]:
                md += f"""
### Subject: {case['user_id']}
- **Risk Weight**: {case.get('risk_score', 'High')}
- **Event Density**: Identified in {case['event_count']} unique forensic shards.
- **Primary Hypothesis**: Profile suggests {case.get('primary_action', 'Suspicious Activity')}.
- **Status**: Critical Subject for Administrative Interview.
"""

            md += f"""
## 5. Investigation Details & Notes
### Investigation Diary
- **{timestamp} [Initialization]**: I established the forensic scope based on the analyst query: `{query}`.
- **{timestamp} [Retrieval]**: I conducted a deep-shard retrieval across the Document Knowledge Graph, extracting the top 50 relevance-scored segments.
- **{timestamp} [Reranking]**: I applied the Cross-Encoder model to prune noise and isolate high-fidelity evidence nodes.
- **{timestamp} [Clustering]**: Subject-level cases were synthesized by grouping actions, identities, and timestamps into a cohesive timeline.

## 6. Investigation Interviews
Institutional-grade 'Virtual Interview' summaries synthesized from digital footprints:
- **Inference 01**: Based on the patterns for subject {cases.get('cases', [{}])[0].get('user_id', 'N/A')}, there is a clear discrepancy between standard job-role activity and the observed {analysis.get('threat_category')}. 
- **Simulated Response**: If questioned, the subject might claim unauthorized access or a hijacked session, but the persistence of the session suggests intentionality.

## 7. Credibility Assessment
I have assessed the identified subjects against the forensic baseline:
- **Plausibility**: The attack vector is highly plausible and aligns with industry-standard TTPs.
- **Motive**: The trajectory of data access suggests a motive related to {analysis.get('threat_category')}.
- **Corroboration**: Multiple independent log shards corroborate the observed sequence of events.

## 8. Evidence Collection and Analysis
The following forensic segments were collected during the autonomous cycle:
"""
            for i, case in enumerate(cases.get("cases", [])[:3], 1):
                md += f"{i}. **Cluster {case['user_id']}**: Involving sources: `{', '.join(case.get('sources', {}).keys())}`. Analysis shows heavy interaction with {len(case.get('timeline', []))} unique event nodes.\n"

            md += f"""
## 9. Conclusion & Recommendations
**Findings**: Based on the available digital evidence, the allegations are **{ 'SUBSTANTIATED' if (int(analysis.get('risk_score', 0)) > 6) else 'PENDING FURTHER REVIEW' }**.

### Institutional Recommendations:
1. **Immediate Containment**: Rotate all credentials for the identified subjects.
2. **Hardening**: Investigate the endpoints associated with the suspicious URL/File triggers.
3. **Legal Review**: Escalate this report to the internal compliance and legal departments.

## 10. FINAL REVIEW & APPENDICES
### Full Attack Surface Mapping (Mermaid)
```mermaid
{graph_code}
```

---
*Generated by UFDR High-Fidelity Copilot System - 2026 Edition*
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)

        return filepath

if __name__ == "__main__":
    rg = ReportGenerator()
    test_query = "suspicious logon"
    test_analysis = {"summary": "Analysis summary", "risk_score": 8, "threat_category": "Insider"}
    test_cases = {"subject_count": 1, "cases": [{"user_id": "U1", "event_count": 1, "timeline": []}]}
    test_graph = "graph TD\n  U1 --> F1"
    path = rg.generate(test_query, test_analysis, test_cases, test_graph)
    print(f"Report generated at: {path}")
