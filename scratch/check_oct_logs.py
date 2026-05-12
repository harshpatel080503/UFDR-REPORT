import sqlite3

db_path = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

user = "AAM0658"
cursor.execute(f"SELECT page_id, date, hour, action, text FROM documents WHERE user = ? AND date LIKE '2010-10%' LIMIT 20", (user,))
print(cursor.fetchall())

conn.close()
