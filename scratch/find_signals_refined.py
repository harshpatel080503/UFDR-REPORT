import sqlite3
import os

DB_PATH = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Data Exfiltration (Wikileaks)
print("--- Data Exfiltration (Wikileaks) ---")
cursor.execute("SELECT user, date, page_id FROM documents WHERE action='visit_url' AND text LIKE '%wikileaks%' LIMIT 5")
exfil = cursor.fetchall()
for r in exfil: print(r)

# 2. Insider Theft (Job Search)
print("\n--- Insider Theft (Job Search) ---")
cursor.execute("SELECT user, date, page_id FROM documents WHERE action='visit_url' AND (text LIKE '%monster.com%' OR text LIKE '%careerbuilder.com%') LIMIT 5")
theft = cursor.fetchall()
for r in theft: print(r)

# 3. Sabotage (Keylogger)
print("\n--- Sabotage (Keylogger) ---")
cursor.execute("SELECT user, date, page_id FROM documents WHERE text LIKE '%keylogger%' LIMIT 5")
sabotage = cursor.fetchall()
for r in sabotage: print(r)

# 4. USB Activity (Common Indicator)
print("\n--- USB Activity ---")
cursor.execute("SELECT user, date, page_id FROM documents WHERE action LIKE '%usb%' OR action LIKE '%removable%' LIMIT 5")
usb = cursor.fetchall()
for r in usb: print(r)

conn.close()
