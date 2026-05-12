import numpy as np
import os

ids_path = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\faiss\non_http_ids.npy"

if os.path.exists(ids_path):
    ids = np.load(ids_path, allow_pickle=True)
    print(f"Total IDs in non_http: {len(ids)}")
    print(f"Sample IDs: {ids[:20]}")
    
    # Check for "logon_001403"
    test_id = "logon_001403"
    if test_id in ids:
        print(f"{test_id} found in non_http IDs!")
    else:
        print(f"{test_id} NOT found in non_http IDs.")
        # Check if they have a prefix or something
        logon_ids = [id for id in ids if str(id).startswith("logon_")]
        print(f"Number of logon_ IDs: {len(logon_ids)}")
        if logon_ids:
            print(f"Sample logon IDs: {logon_ids[:5]}")
else:
    print("File not found.")
