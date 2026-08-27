import sqlite3
import os
import threading
from uniface.core.config import ROOT_DIR

_db_lock = threading.Lock()
_db_path = os.path.join(ROOT_DIR, "workspace", "uniface.db")

def init_db():
    os.makedirs(os.path.dirname(_db_path), exist_ok=True)
    with _db_lock:
        conn = sqlite3.connect(_db_path)
        cursor = conn.cursor()
        
        # Table to store known hashes and their canonical pool paths
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS target_hashes (
            hash TEXT PRIMARY KEY,
            pool_path TEXT NOT NULL,
            size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()

def get_hash_path(file_hash: str) -> str:
    """Returns the pool path for a given hash, or None if not found."""
    with _db_lock:
        conn = sqlite3.connect(_db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT pool_path FROM target_hashes WHERE hash = ?', (file_hash,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return None

def register_hash(file_hash: str, pool_path: str, size: int):
    """Registers a new hash and its pool path."""
    with _db_lock:
        conn = sqlite3.connect(_db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO target_hashes (hash, pool_path, size) VALUES (?, ?, ?)',
            (file_hash, pool_path, size)
        )
        conn.commit()
        conn.close()

def remove_hash(file_hash: str):
    """Removes a hash from the registry (e.g. if the pool file is deleted)."""
    with _db_lock:
        conn = sqlite3.connect(_db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM target_hashes WHERE hash = ?', (file_hash,))
        conn.commit()
        conn.close()
