import sqlite3

db_path = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Checking for logon_ IDs...")
cursor.execute("SELECT page_id FROM documents WHERE page_id LIKE 'logon_%' LIMIT 5")
print(cursor.fetchall())

print("Checking for device_ IDs...")
cursor.execute("SELECT page_id FROM documents WHERE page_id LIKE 'device_%' LIMIT 5")
print(cursor.fetchall())

print("Checking for http_ IDs...")
cursor.execute("SELECT page_id FROM documents WHERE page_id LIKE 'http_%' LIMIT 5")
print(cursor.fetchall())

conn.close()
