import json
import os
from datetime import datetime

# Configuration
INPUT_DIR = "E:/Data Science Study/Deep Learning Project/UFDR/processed data/Data"
OUTPUT_DIR = "E:/Data Science Study/Deep Learning Project/UFDR/processed data/PageIndex_Data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Action Mapping
def map_action(event_type, record):
    if event_type == "email":
        return "send_email"
    elif event_type == "logon":
        return "login"
    elif event_type == "device":
        return "connect_device" if "Connect" in record.get("text", "") else "disconnect_device"
    elif event_type == "file":
        return "file_copy"
    elif event_type == "http":
        return "visit_url"
    elif event_type == "ldap":
        return "user_metadata"
    else:
        return "unknown"

# Extracting Time Series
def extract_time_features(timestamp):
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d"), dt.hour
    except:
        return None, None

# Normalizing Text
def normalize_text(record):
    user = record.get("user", "")
    action = record.get("action", "")
    return f"{user} performed {action}"

# Processing File
def process_file(file_path, output_path, prefix):
    print(f"Processing {file_path}")

    with open(file_path, "r", encoding="utf-8") as f_in, \
         open(output_path, "w", encoding="utf-8") as f_out:

        for i, line in enumerate(f_in):
            try:
                record = json.loads(line)

                # Page Indexing
                record["page_id"] = f"{prefix}_{i:06d}"
                record["source_file"] = os.path.basename(file_path)
                record["line_number"] = i

                # Time Features
                timestamp = record.get("timestamp", "")
                date, hour = extract_time_features(timestamp)
                record["date"] = date
                record["hour"] = hour

                # Action
                event_type = record.get("event_type", "")
                record["action"] = map_action(event_type, record)

                # Target Users
                entities = record.get("entities", {})
                record["target_users"] = entities.get("users", [])

                # Objects
                record["objects"] = [event_type]

                # Keywords
                keyword_map = {
                    "email": ["communication"],
                    "file": ["file_transfer"],
                    "device": ["usb_activity"],
                    "http": ["web_activity"],
                    "logon": ["authentication"]
                }
                record["keywords"] = keyword_map.get(event_type, [])

                # Normalized Text
                record["normalized_text"] = normalize_text(record)

                # Write
                f_out.write(json.dumps(record) + "\n")

            except Exception as e:
                continue

    print(f"Done: {output_path}")


# MAIN
def main():
    files = {
        "email.jsonl": "email",
        "logon.jsonl": "logon",
        "device.jsonl": "device",
        "file.jsonl": "file",
        "http.jsonl": "http",
        "ldap.jsonl": "ldap",
        "psychometric.jsonl": "psychometric"
    }

    for file_name, prefix in files.items():
        input_path = os.path.join(INPUT_DIR, file_name)
        output_path = os.path.join(OUTPUT_DIR, file_name)

        if os.path.exists(input_path):
            process_file(input_path, output_path, prefix)

    print("\nALL FILES CONVERTED TO PAGEINDEX FORMAT")


if __name__ == "__main__":
    main()