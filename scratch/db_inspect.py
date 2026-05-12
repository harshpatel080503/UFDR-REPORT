import sqlite3
import os

db_path = r"e:\Data Science Study\Deep Learning Project\UFDR\Indexing\output\page_index.db"

if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    
    if tables:
        table_name = tables[0][0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"Columns in {table_name}: {[c[1] for c in columns]}")
        
        cursor.execute(f"SELECT page_id FROM {table_name} LIMIT 10")
        sample_ids = cursor.fetchall()
        print(f"Sample page_ids: {[s[0] for s in sample_ids]}")
        
        # Check for a specific ID from golden dataset
        # "logon_001403"
        test_id = "logon_001403"
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE page_id = ?", (test_id,))
        count = cursor.fetchone()[0]
        print(f"Count for {test_id}: {count}")
        
        # Check if they have a different prefix or format
        cursor.execute(f"SELECT page_id FROM {table_name} WHERE page_id LIKE '%001403%' LIMIT 5")
        similar = cursor.fetchall()
        print(f"Similar to 001403: {[s[0] for s in similar]}")

    conn.close()
