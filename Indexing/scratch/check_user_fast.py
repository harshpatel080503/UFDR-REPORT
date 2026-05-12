import sqlite3
db = r'e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db'
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute("SELECT count(*) FROM documents WHERE user = 'CDE1846';")
print(f"Exact match 'CDE1846': {cur.fetchone()[0]}")
cur.execute("SELECT count(*) FROM documents WHERE user = 'cde1846';")
print(f"Exact match 'cde1846': {cur.fetchone()[0]}")
conn.close()
