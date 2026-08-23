"""
Caching mechanism using SQLite for pipeline idempotency and fast re-runs.
"""
import os
import sqlite3
import json
from typing import Optional, Any

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pipeline_cache.db")

def init_cache(db_path: str = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            cache_key TEXT PRIMARY KEY,
            data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_cache(cache_key: str, db_path: str = DB_PATH) -> Optional[Any]:
    if not os.path.exists(db_path):
        return None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM cache WHERE cache_key = ?", (cache_key,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return json.loads(row[0])
    except Exception:
        pass
    return None

def set_cache(cache_key: str, data: Any, db_path: str = DB_PATH) -> None:
    init_cache(db_path)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO cache (cache_key, data) VALUES (?, ?)",
            (cache_key, json.dumps(data, ensure_ascii=False))
        )
        conn.commit()
        conn.close()
    except Exception:
        pass
