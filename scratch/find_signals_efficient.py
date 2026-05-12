import sqlite3
import os

DB_PATH = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Fast search using action_index
def find_signal(action, text_pattern, label):
    print(f"--- {label} ---")
    query = f"""
    SELECT d.user, d.date, d.page_id 
    FROM action_index a
    JOIN documents d ON a.page_id = d.page_id
    WHERE a.action = ? AND d.text LIKE ?
    LIMIT 5
    """
    cursor.execute(query, (action, text_pattern))
    res = cursor.fetchall()
    for r in res: print(r)
    return res

find_signal('visit_url', '%wikileaks%', 'Data Exfiltration')
find_signal('visit_url', '%monster.com%', 'Insider Theft')
find_signal('file_copy', '%keylogger%', 'Sabotage')
find_signal('device_connect', '%%', 'USB Activity')

conn.close()
