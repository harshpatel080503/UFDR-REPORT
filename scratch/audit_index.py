import sqlite3
import os

db_path = r'e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db'
if not os.path.exists(db_path):
    print(f"Error: {db_path} not found")
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

print(f"{'Source':<15} | {'Count':<10} | {'Min Date':<12} | {'Max Date':<12}")
print("-" * 55)

cur.execute('SELECT source, count(*), min(date), max(date) FROM documents GROUP BY source')
for row in cur.fetchall():
    source, count, min_date, max_date = row
    print(f"{str(source):<15} | {count:<10,} | {str(min_date):<12} | {str(max_date):<12}")

# Check for Nulls or anomalies
cur.execute('SELECT count(*) FROM documents WHERE user IS NULL OR user = ""')
null_users = cur.fetchone()[0]
print(f"\nDocuments with empty User: {null_users:,}")

cur.execute('SELECT count(*) FROM documents WHERE text IS NULL OR text = ""')
null_text = cur.fetchone()[0]
print(f"Documents with empty Text: {null_text:,}")

conn.close()
