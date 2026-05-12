import sqlite3
import os
import json
import time

try:
    import orjson
    def _parse(line: str):
        return orjson.loads(line)
except ImportError:
    def _parse(line: str):
        return json.loads(line)

from config import (
    PAGEINDEX_DB,
    SQLITE_BATCH,
    STORE_FULL_RECORD,
)


class PageIndexBuilder:

    def __init__(self, db_path: str = PAGEINDEX_DB, allowed_pids: set | None = None):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.allowed_pids = allowed_pids

        self.conn.execute("PRAGMA journal_mode  = WAL")
        self.conn.execute("PRAGMA synchronous   = OFF")  # Optimized for bulk ingestion
        self.conn.execute("PRAGMA cache_size    = -128000") # 128MB cache
        self.conn.execute("PRAGMA temp_store    = MEMORY")
        self.conn.execute("PRAGMA mmap_size     = 1073741824") # 1GB mmap

        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()

        # Redundant index tables removed. Data is indexed directly in 'documents' table.
        pass

        cols = (
            "page_id TEXT PRIMARY KEY, "
            "source TEXT, "
            "user TEXT, "
            "action TEXT, "
            "date TEXT, "
            "hour INTEGER, "
            "event_type TEXT, "
            "text TEXT, "
            "normalized_text TEXT"
        )
        if STORE_FULL_RECORD:
            cols += ", full_record TEXT"

        c.execute(f"CREATE TABLE IF NOT EXISTS documents ({cols})")
        self.conn.commit()

    def process_file(self, file_path: str, source: str) -> int:
        print(f"\n{'-' * 60}")
        print(f"  PageIndex > {source}")
        print(f"  {file_path}")
        print(f"{'-' * 60}")

        t0 = time.time()
        n  = 0

        buf_doc: list = []

        with open(file_path, "r", encoding="utf-8") as fh:
            for raw_line in fh:
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                try:
                    rec = _parse(raw_line)
                except Exception:
                    continue

                pid  = rec.get("page_id", "")
                if self.allowed_pids is not None and pid not in self.allowed_pids:
                    continue

                user = rec.get("user", "")
                act  = rec.get("action", "")
                dt   = rec.get("date", "")
                hr   = rec.get("hour")
                evt  = rec.get("event_type", "")
                txt  = rec.get("text", "")
                ntxt = rec.get("normalized_text", "")

                # Buffers for redundant tables removed
                pass

                if STORE_FULL_RECORD:
                    buf_doc.append(
                        (pid, source, user, act, dt, hr, evt, txt, ntxt, raw_line)
                    )
                else:
                    buf_doc.append(
                        (pid, source, user, act, dt, hr, evt, txt, ntxt)
                    )

                n += 1

                if n % SQLITE_BATCH == 0:
                    self._flush(buf_doc)
                    buf_doc = []

                if n % 500_000 == 0:
                    elapsed = time.time() - t0
                    print(f"    {n:>12,} rows   ({n / elapsed:,.0f} rows/s)")

        if buf_doc:
            self._flush(buf_doc)

        elapsed = time.time() - t0
        print(f"  {n:,} rows in {elapsed:.1f}s   ({n / elapsed:,.0f} rows/s)")
        return n

    def _flush(self, bdoc):
        c = self.conn.cursor()
        if STORE_FULL_RECORD:
            c.executemany(
                "INSERT OR IGNORE INTO documents VALUES (?,?,?,?,?,?,?,?,?,?)",
                bdoc,
            )
        else:
            c.executemany(
                "INSERT OR IGNORE INTO documents VALUES (?,?,?,?,?,?,?,?,?)",
                bdoc,
            )
        self.conn.commit()

    def build_sql_indexes(self):
        print(f"\n{'-' * 60}")
        print("  Building SQL indexes ...")
        print(f"{'-' * 60}")

        t0 = time.time()
        defs = [
            ("ix_doc_pageid", "documents(page_id)"),
            ("ix_doc_user",   "documents(user)"),
            ("ix_doc_date",   "documents(date)"),
            ("ix_doc_action", "documents(action)"),
            ("ix_doc_src",    "documents(source)"),
        ]
        c = self.conn.cursor()
        for name, cols in defs:
            print(f"    {name} …")
            c.execute(f"CREATE INDEX IF NOT EXISTS {name} ON {cols}")

        self.conn.commit()
        print(f"All indexes built in {time.time() - t0:.1f}s")

    def get_source_counts(self) -> dict:
        """Returns a dictionary of source -> row_count from the documents table."""
        try:
            c = self.conn.cursor()
            c.execute("SELECT source, COUNT(*) FROM documents GROUP BY source")
            return dict(c.fetchall())
        except sqlite3.OperationalError:
            # Table might not exist yet
            return {}

    def print_stats(self):
        print(f"\n{'-' * 60}")
        print("  PageIndex Statistics")
        print(f"{'-' * 60}")

        c = self.conn.cursor()
        for tbl in ("documents",):
            c.execute(f"SELECT COUNT(*) FROM {tbl}")
            print(f"    {tbl:>20s}: {c.fetchone()[0]:>15,}")

        counts = self.get_source_counts()
        print()
        for src, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            print(f"    {src:>20s}: {cnt:>15,}")

    def query_by_user(self, user: str):
        c = self.conn.cursor()
        c.execute("SELECT page_id FROM documents WHERE user = ?", (user,))
        return [row[0] for row in c.fetchall()]

    def query_by_date(self, date: str):
        c = self.conn.cursor()
        c.execute("SELECT page_id FROM documents WHERE date = ?", (date,))
        return [row[0] for row in c.fetchall()]

    def query_by_action(self, action: str):
        c = self.conn.cursor()
        c.execute("SELECT page_id FROM documents WHERE action = ?", (action,))
        return [row[0] for row in c.fetchall()]

    def query_by_hour(self, hour: int):
        c = self.conn.cursor()
        c.execute("SELECT page_id FROM documents WHERE hour = ?", (hour,))
        return [row[0] for row in c.fetchall()]

    def get_document(self, page_id: str) -> dict:
        c = self.conn.cursor()
        c.execute("SELECT * FROM documents WHERE page_id = ?", (page_id,))
        row = c.fetchone()
        if row is None:
            return {}
        cols = [desc[0] for desc in c.description]
        return dict(zip(cols, row))

    def get_documents_batch(self, page_ids: list) -> list:
        if not page_ids:
            return []
        placeholders = ",".join("?" for _ in page_ids)
        c = self.conn.cursor()
        c.execute(
            f"SELECT * FROM documents WHERE page_id IN ({placeholders})",
            page_ids,
        )
        cols = [desc[0] for desc in c.description]
        return [dict(zip(cols, row)) for row in c.fetchall()]

    def close(self):
        self.conn.close()
