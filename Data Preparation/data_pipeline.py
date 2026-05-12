import pandas as pd
import json
import uuid
import os
from glob import glob

# Configuration
DATA_PATH = "E:/Data Science Study/Deep Learning Project/UFDR/raw data/r4.2"
OUTPUT_DIR = "E:/Data Science Study/Deep Learning Project/UFDR/processed data"
CHUNK_SIZE = 100000
BATCH_SIZE = 5000

START_DATE = "2010-01-01"
END_DATE = "2010-06-30"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Helping function
def generate_id():
    return str(uuid.uuid4())

def safe_split(x):
    if pd.isna(x):
        return []
    return [i.strip() for i in str(x).split(";") if i.strip()]

def write_batch(batch, file_path):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n".join(json.dumps(x) for x in batch) + "\n")

def filter_time(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df[
        (df["date"] >= START_DATE) &
        (df["date"] <= END_DATE)
    ]

# Processing Pipeline
def process_stream(input_file, output_file, transform_fn):
    print(f"Processing {input_file}")

    for chunk in pd.read_csv(
        f"{DATA_PATH}/{input_file}",
        chunksize=CHUNK_SIZE,
        engine="c",
        low_memory=True
    ):
        chunk = filter_time(chunk)

        batch = []

        for row in chunk.itertuples(index=False):
            try:
                record = transform_fn(row)
                batch.append(record)

                if len(batch) >= BATCH_SIZE:
                    write_batch(batch, output_file)
                    batch = []

            except Exception:
                continue

        if batch:
            write_batch(batch, output_file)

# Transform function
def email_transform(row):
    return {
        "doc_id": generate_id(),
        "timestamp": str(row.date),
        "user": row.user,
        "pc": row.pc,
        "event_type": "email",
        "text": f"{row.user} emailed {row.to} content {row.content[:200]}",
        "entities": {
            "users": safe_split(row.to) + safe_split(row.cc) + safe_split(row.bcc),
            "devices": [row.pc]
        },
        "metadata": {"size": row.size}
    }

def logon_transform(row):
    return {
        "doc_id": generate_id(),
        "timestamp": str(row.date),
        "user": row.user,
        "pc": row.pc,
        "event_type": "logon",
        "text": f"{row.user} {row.activity} on {row.pc}",
        "entities": {"users": [row.user]},
        "metadata": {}
    }

def device_transform(row):
    return {
        "doc_id": generate_id(),
        "timestamp": str(row.date),
        "user": row.user,
        "pc": row.pc,
        "event_type": "device",
        "text": f"{row.user} {row.activity} device on {row.pc}",
        "entities": {"users": [row.user]},
        "metadata": {}
    }

def file_transform(row):
    return {
        "doc_id": generate_id(),
        "timestamp": str(row.date),
        "user": row.user,
        "pc": row.pc,
        "event_type": "file",
        "text": f"{row.user} accessed {row.filename} content {row.content[:150]}",
        "entities": {"files": [row.filename]},
        "metadata": {}
    }

def http_transform(row):
    return {
        "doc_id": generate_id(),
        "timestamp": str(row.date),
        "user": row.user,
        "pc": row.pc,
        "event_type": "http",
        "text": f"{row.user} visited {row.url} content {row.content[:100]}",
        "entities": {"urls": [row.url]},
        "metadata": {}
    }

# LDAP and Psychometric
def process_ldap():
    print("Processing LDAP")

    output_file = f"{OUTPUT_DIR}/ldap.jsonl"

    for file in glob(f"{DATA_PATH}/LDAP/*.csv"):
        df = pd.read_csv(file)

        batch = []
        for row in df.itertuples(index=False):
            batch.append({
                "doc_id": generate_id(),
                "timestamp": file.split("/")[-1],
                "user": row.user_id,
                "event_type": "ldap",
                "text": f"{row.employee_name} role {row.role} dept {row.department}",
                "entities": {"users": [row.user_id]},
                "metadata": {}
            })

        write_batch(batch, output_file)

def process_psychometric():
    print("Processing Psychometric")

    df = pd.read_csv(f"{DATA_PATH}/psychometric.csv")
    output_file = f"{OUTPUT_DIR}/psychometric.jsonl"

    batch = []
    for row in df.itertuples(index=False):
        batch.append({
            "doc_id": generate_id(),
            "user": row.user_id,
            "event_type": "psychometric",
            "text": f"user {row.user_id} personality scores",
            "entities": {"users": [row.user_id]},
            "metadata": {}
        })

    write_batch(batch, output_file)

# Main
if __name__ == "__main__":

    process_stream("email.csv", f"{OUTPUT_DIR}/email.jsonl", email_transform)
    process_stream("logon.csv", f"{OUTPUT_DIR}/logon.jsonl", logon_transform)
    process_stream("device.csv", f"{OUTPUT_DIR}/device.jsonl", device_transform)
    process_stream("file.csv", f"{OUTPUT_DIR}/file.jsonl", file_transform)
    process_stream("http.csv", f"{OUTPUT_DIR}/http.jsonl", http_transform)

    process_ldap()
    process_psychometric()

    print("\nDONE - dataset ready")