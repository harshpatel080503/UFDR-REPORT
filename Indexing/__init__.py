"""
UFDR Indexing Package
=====================
Hybrid indexing system for the UFDR Copilot forensic evidence retrieval pipeline.

Modules
-------
* ``page_index``       — SQLite-backed inverted indexes (user, action, date, hour)
* ``embedding_engine`` — Sentence-transformer embedding generation with checkpointing
* ``faiss_builder``    — FAISS IVF+PQ index construction and search
* ``pipeline``         — End-to-end orchestrator
* ``config``           — Central configuration

Quick start
-----------
::

    cd UFDR/Indexing
    pip install -r requirements.txt
    python pipeline.py              # run all phases
    python pipeline.py --phase pageindex   # just Phase 1
"""

from .page_index import PageIndexBuilder
from .faiss_builder import FAISSBuilder, FAISSSearcher

__all__ = ["PageIndexBuilder", "FAISSBuilder", "FAISSSearcher"]
