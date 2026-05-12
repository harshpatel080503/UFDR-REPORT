import sqlite3
import os

db_path = r"E:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
if not os.path.exists(db_path):
    print(f"File not found: {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    for table in tables:
        tname = table[0]
        print(f"\nSchema for {tname}:")
        cursor.execute(f"PRAGMA table_info({tname})")
        cols = cursor.fetchall()
        for col in cols:
            print(col)
    conn.close()
