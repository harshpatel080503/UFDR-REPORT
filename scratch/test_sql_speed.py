import sqlite3
import time

DB_PATH = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

t0 = time.time()
user = "AAM0658"
s = "2010-01-01"
e = "2010-06-29"
cursor.execute("SELECT page_id FROM documents WHERE user = ? AND date >= ? AND date <= ? LIMIT 5", (user, s, e))
print(cursor.fetchall())
print(f"Time: {time.time()-t0:.4f}s")
conn.close()
