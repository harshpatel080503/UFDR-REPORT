import sqlite3
import csv
from datetime import datetime

DB_PATH = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"
INSIDERS_CSV = r"e:\Data Science Study\Deep Learning Project\UFDR\Data\processed data\Insiders Ground Truth Labels\insiders.csv"

def parse_date(d):
    for fmt in ("%m/%d/%Y %H:%M:%S", "%m/%d/%Y", "%Y-%m-%d"):
        try: return datetime.strptime(d.strip(), fmt)
        except: continue
    return None

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

limit_date = datetime(2010, 6, 29)
with open(INSIDERS_CSV, "r") as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        d = parse_date(row["start"])
        if d and d <= limit_date:
            user = row["user"]
            s = d.strftime("%Y-%m-%d")
            print(f"User: {user}, Date: {s}", flush=True)
            cursor.execute("SELECT page_id FROM documents WHERE user = ? AND date = ? LIMIT 5", (user, s))
            logs = cursor.fetchall()
            print(f"  Logs: {logs}", flush=True)
            count += 1
            if count >= 11: break
conn.close()
