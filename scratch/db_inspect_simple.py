import sqlite3
import os

db_path = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Getting tables...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

print("Getting columns of documents...")
cursor.execute("PRAGMA table_info(documents)")
print(cursor.fetchall())

print("Getting sample IDs...")
cursor.execute("SELECT page_id FROM documents LIMIT 20")
print(cursor.fetchall())

conn.close()
