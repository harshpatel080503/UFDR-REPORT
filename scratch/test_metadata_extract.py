import re
from datetime import datetime

def extract_metadata(query):
    # Extract User ID like AAM0658
    user_match = re.search(r'[A-Z]{3}\d{4}', query)
    user = user_match.group(0) if user_match else None
    
    # Extract Date like 2010-10-23
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', query)
    date = date_match.group(0) if date_match else None
    
    return user, date

queries = [
    "Show activity for AAM0658 on 2010-06-28",
    "Did user JMB0308 visit wikileaks?",
    "Investigate 2010-05-15 logs"
]

for q in queries:
    u, d = extract_metadata(q)
    print(f"Query: {q} -> User: {u}, Date: {d}")
