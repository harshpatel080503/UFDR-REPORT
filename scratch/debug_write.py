import os
import datetime

output_dir = "Reports"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
filename = f"DEBUG_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
filepath = os.path.join(output_dir, filename)

print(f"Writing to: {os.path.abspath(filepath)}")
with open(filepath, "w", encoding="utf-8") as f:
    f.write(f"Debug report at {timestamp}")

print("Done. Checking directory...")
print(os.listdir(output_dir))
