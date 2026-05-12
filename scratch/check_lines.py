import json
import os

fpath = r"E:\Data Science Study\Deep Learning Project\UFDR\Data\processed data\PageIndex_Data\http.jsonl"
start_line = 3265353
count = 10

with open(fpath, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < start_line:
            continue
        if i >= start_line + count:
            break
        try:
            rec = json.loads(line)
            print(f"Line {i}: {rec.get('date', 'N/A')}")
        except:
            print(f"Line {i}: Error parsing")
