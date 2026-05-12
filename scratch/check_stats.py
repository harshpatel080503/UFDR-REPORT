import sqlite3
import os

db_path = r"E:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT source, COUNT(*) FROM documents GROUP BY source")
    for src, cnt in c.fetchall():
        print(f"{src}: {cnt:,}")
    conn.close()
else:
    print("DB not found")
