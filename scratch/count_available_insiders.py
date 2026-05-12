import csv
import os
from datetime import datetime

base = r"e:\Data Science Study\Deep Learning Project\UFDR"
insiders_csv = os.path.join(base, "Data", "processed data", "Insiders Ground Truth Labels", "insiders.csv")

def parse_date(d):
    for fmt in ("%m/%d/%Y %H:%M:%S", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(d.strip(), fmt)
        except:
            continue
    return None

available_count = 0
total_count = 0
limit_date = datetime(2010, 6, 29)

with open(insiders_csv, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_count += 1
        start = parse_date(row["start"])
        if start and start <= limit_date:
            available_count += 1
            # print(f"Available: {row['user']} ({row['scenario']}) - {row['start']}")

print(f"Total insiders: {total_count}")
print(f"Insiders within indexed range (<= 2010-06-29): {available_count}")
