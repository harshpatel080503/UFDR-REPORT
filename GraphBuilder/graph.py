import re

class GraphBuilder:
    def __init__(self):
        self.patterns = {
            "url": re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+'),
            "file": re.compile(r'[a-zA-Z0-9_\-.]+\.(?:exe|doc|txt|pdf|zip|asp|php|html|jsp|csv)', re.IGNORECASE),
            "ip": re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),
            "device": re.compile(r'(PC|DEVICE|COMP)-\d{4}', re.IGNORECASE)
        }

    def _clean_id(self, raw_id):
        return re.sub(r'[^a-zA-Z0-9_]', '_', str(raw_id))

    def generate_graph(self, evidence, ai_knowledge=None):
        if not evidence and not ai_knowledge:
            return "graph TD\n  Start[No Evidence]"

        nodes = {}
        edges = set()

        for rec in evidence:
            user = rec.get("user", "UnknownUser")
            u_id = f"U_{self._clean_id(user)}"
            nodes[u_id] = f"User: {user}"
            
            text = rec.get("text", "")
            action = rec.get("action", "activity")
            
            urls = self.patterns["url"].findall(text)
            for url in urls:
                domain = url.split("//")[-1].split("/")[0]
                node_id = f"URL_{self._clean_id(domain)}"
                nodes[node_id] = f"URL: {domain}"
                edges.add(f'  {u_id} --"{action}"--> {node_id}')

            files = self.patterns["file"].findall(text)
            for file in files:
                node_id = f"FILE_{self._clean_id(file)}"
                nodes[node_id] = f"File: {file}"
                edges.add(f'  {u_id} --"{action}"--> {node_id}')

            ips = self.patterns["ip"].findall(text)
            for ip in ips:
                node_id = f"IP_{self._clean_id(ip)}"
                nodes[node_id] = f"IP: {ip}"
                edges.add(f'  {u_id} --"{action}"--> {node_id}')

        if ai_knowledge:
            for ent in ai_knowledge.get("entities", []):
                ent_id = ent.get("id")
                if not ent_id: continue
                
                clean_id = f"AI_{self._clean_id(ent_id)}"
                label = ent.get("label", ent_id)
                ent_type = ent.get("type", "Entity")
                
                nodes[clean_id] = f"{ent_type}: {label}"

            for rel in ai_knowledge.get("relationships", []):
                src = rel.get("source")
                tgt = rel.get("target")
                label = rel.get("relation", "links")
                
                if src and tgt:
                    s_id = f"U_{self._clean_id(src)}" if f"U_{self._clean_id(src)}" in nodes else f"AI_{self._clean_id(src)}"
                    t_id = f"URL_{self._clean_id(tgt)}" if f"URL_{self._clean_id(tgt)}" in nodes else f"AI_{self._clean_id(tgt)}"
                    
                    if s_id not in nodes: s_id = f"AI_{self._clean_id(src)}"
                    if t_id not in nodes: t_id = f"AI_{self._clean_id(tgt)}"
                    
                    edges.add(f'  {s_id} --"{label}"--> {t_id}')

        mermaid_code = ["graph LR"]
        for nid, label in nodes.items():
            if nid.startswith("AI_"):
                 mermaid_code.append(f'  {nid}(("{label}"))')
            else:
                 mermaid_code.append(f'  {nid}["{label}"]')
        
        mermaid_code.extend(list(edges))
        
        return "\n".join(mermaid_code)

if __name__ == "__main__":
    bg = GraphBuilder()
    test_data = [
        {"user": "CSC0217", "action": "file_copy", "text": "accessed secret.doc on PC-1234"},
        {"user": "CSC0217", "action": "visit_url", "text": "visited http://malware.com/virus.exe"}
    ]
    code = bg.generate_graph(test_data)
    print("Mermaid Code:")
    print(code)
