import sqlite3
import os

DB_PATH = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

patterns = {
    "Data Exfiltration": "%wikileaks%",
    "Insider Theft": "%monster.com%",
    "Sabotage": "%keylogger%"
}

print(f"{'Category':<20} | {'User':<10} | {'Date':<12} | {'Log ID'}")
print("-" * 60)

for cat, pat in patterns.items():
    cursor.execute("SELECT user, date, page_id, text FROM documents WHERE text LIKE ? LIMIT 5", (pat,))
    for user, date, pid, text in cursor.fetchall():
        print(f"{cat:<20} | {user:<10} | {date:<12} | {pid}")

# Also check for USB
print("\nUSB Activity:")
cursor.execute("SELECT user, date, page_id FROM documents WHERE action LIKE '%usb%' OR action LIKE '%removable%' LIMIT 5")
for user, date, pid in cursor.fetchall():
    print(f"{'USB':<20} | {user:<10} | {date:<12} | {pid}")

conn.close()
