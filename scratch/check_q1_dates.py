import sqlite3

db_path = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

ids = ["logon_001403", "logon_002778", "logon_003973", "logon_005388", "logon_006521"]
placeholders = ",".join("?" for _ in ids)
cursor.execute(f"SELECT page_id, date, user, action FROM documents WHERE page_id IN ({placeholders})", ids)
print(cursor.fetchall())

conn.close()
