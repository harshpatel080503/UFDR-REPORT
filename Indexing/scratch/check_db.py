import sqlite3
import os

db = r'e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db'
if not os.path.exists(db):
    print("Database not found!")
    exit(1)

conn = sqlite3.connect(db)
cur = conn.cursor()

print("--- Checking for user CDE1846 ---")
cur.execute("SELECT source, COUNT(*) FROM documents WHERE user LIKE '%CDE1846%' GROUP BY source;")
results = cur.fetchall()
if not results:
    print("No records found for CDE1846.")
else:
    for source, count in results:
        print(f"  Source: {source:<15} | Records: {count:,}")

print("\n--- Checking available sources in DB ---")
cur.execute("SELECT source, COUNT(*) FROM documents GROUP BY source;")
for source, count in cur.fetchall():
    print(f"  {source:<20}: {count:,} rows")

conn.close()
