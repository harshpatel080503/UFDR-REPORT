import sqlite3

db_path = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check for logon events in October 2010
cursor.execute("SELECT COUNT(*) FROM documents WHERE page_id LIKE 'logon_%' AND date LIKE '2010-10%'")
print(f"Logon events in October 2010: {cursor.fetchone()[0]}")

# Check for device events in October 2010
cursor.execute("SELECT COUNT(*) FROM documents WHERE page_id LIKE 'device_%' AND date LIKE '2010-10%'")
print(f"Device events in October 2010: {cursor.fetchone()[0]}")

conn.close()
