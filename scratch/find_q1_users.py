import sqlite3
db_path = r'e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT user, count(*) as c FROM documents WHERE date BETWEEN '2010-01-01' AND '2010-03-31' GROUP BY user ORDER BY c DESC LIMIT 5")
print("Top users in Q1 2010:")
for row in cur.fetchall():
    print(f"User: {row[0]}, Events: {row[1]}")
conn.close()
