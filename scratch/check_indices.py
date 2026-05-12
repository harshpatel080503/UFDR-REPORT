import sqlite3
db_path = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA index_list(documents)")
print(cursor.fetchall())
conn.close()
