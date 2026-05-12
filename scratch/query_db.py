import sqlite3
import os

db_path = r'E:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT page_id, date, user, text FROM documents WHERE user='FEB0306' AND date LIKE '2010-01-%'")
rows = cur.fetchall()
print(f"Found {len(rows)} rows for FEB0306 in Jan 2010")
for row in rows:
    print(row)

conn.close()
