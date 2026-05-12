import sqlite3

db_path = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def check_prefix(prefix):
    print(f"Checking for {prefix} IDs...")
    # Use range query to force index usage
    cursor.execute(f"SELECT page_id FROM documents WHERE page_id >= ? AND page_id <= ? LIMIT 5", (prefix, prefix + "\uffff"))
    print(cursor.fetchall())

check_prefix("logon_")
check_prefix("device_")
check_prefix("http_")
check_prefix("email_")
check_prefix("file_")

conn.close()
