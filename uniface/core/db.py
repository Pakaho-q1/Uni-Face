import sqlite3
import os
import json
import threading
from typing import Optional, List, Dict, Any
from uniface.core.config import ROOT_DIR

_db_lock = threading.Lock()
_db_path = os.path.join(ROOT_DIR, "workspace", "uniface.db")
_local = threading.local()

def _is_connection_open(conn):
    if conn is None:
        return False
    try:
        conn.total_changes
        return True
    except (sqlite3.ProgrammingError, sqlite3.OperationalError):
        return False

def _get_connection():
    current_path = getattr(_local, "db_path", None)
    conn = getattr(_local, "connection", None)
    if conn is not None:
        if current_path != _db_path or not _is_connection_open(conn):
            try:
                conn.close()
            except Exception:
                pass
            conn = None
            _local.connection = None
            _local.db_path = None

    if conn is None:
        conn = sqlite3.connect(_db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute('PRAGMA journal_mode=WAL;')
            conn.execute('PRAGMA synchronous=NORMAL;')
        except Exception:
            pass
        _local.connection = conn
        _local.db_path = _db_path
    return conn

def close_thread_connection():
    conn = getattr(_local, "connection", None)
    if conn is not None:
        try:
            conn.close()
        except Exception:
            pass
        _local.connection = None
        _local.db_path = None

def init_db():
    os.makedirs(os.path.dirname(_db_path), exist_ok=True)
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        
        # Optimize performance with WAL journal mode
        try:
            cursor.execute('PRAGMA journal_mode=WAL;')
        except Exception:
            pass

        # Table to store known hashes and their canonical pool paths
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS target_hashes (
            hash TEXT PRIMARY KEY,
            pool_path TEXT NOT NULL,
            size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Table to store background processing jobs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            platform TEXT DEFAULT 'unknown',
            status TEXT DEFAULT 'pending',
            source_type TEXT DEFAULT 'image',
            source_file_id TEXT,
            source_name TEXT,
            target_type TEXT DEFAULT 'upload',
            target_count INTEGER DEFAULT 0,
            target_summary TEXT,
            progress REAL DEFAULT 0.0,
            frames_done INTEGER DEFAULT 0,
            total_frames INTEGER DEFAULT 0,
            output_path TEXT,
            error TEXT,
            config_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Indexes for fast querying & sorting
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at DESC);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_platform ON jobs(platform);')
        
        conn.commit()

# --- Target Hashes Operations ---

def get_hash_path(file_hash: str) -> Optional[str]:
    """Returns the pool path for a given hash, or None if not found."""
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT pool_path FROM target_hashes WHERE hash = ?', (file_hash,))
        result = cursor.fetchone()
        if result:
            return result["pool_path"]
        return None

def register_hash(file_hash: str, pool_path: str, size: int):
    """Registers a new hash and its pool path."""
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO target_hashes (hash, pool_path, size) VALUES (?, ?, ?)',
            (file_hash, pool_path, size)
        )
        conn.commit()

def remove_hash(file_hash: str):
    """Removes a hash from the registry (e.g. if the pool file is deleted)."""
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM target_hashes WHERE hash = ?', (file_hash,))
        conn.commit()

# --- Jobs CRUD Operations ---

def create_job_record(
    job_id: str,
    platform: str = "unknown",
    status: str = "pending",
    source_type: str = "image",
    source_file_id: Optional[str] = None,
    source_name: Optional[str] = None,
    target_type: str = "upload",
    target_count: int = 0,
    target_summary: Optional[str] = None,
    config_json: Optional[str] = None
) -> Dict[str, Any]:
    """Inserts a new job record into SQLite."""
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO jobs (
            id, platform, status, source_type, source_file_id, source_name,
            target_type, target_count, target_summary, config_json,
            progress, frames_done, total_frames, output_path, error,
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0.0, 0, 0, NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', (
            job_id, platform, status, source_type, source_file_id, source_name,
            target_type, target_count, target_summary, config_json
        ))
        conn.commit()
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
        row = cursor.fetchone()
        return dict(row) if row else {}

def update_job_record(job_id: str, updates: Dict[str, Any]) -> bool:
    """Updates specific columns of a job record."""
    if not updates:
        return False
        
    allowed_cols = {
        "status", "progress", "frames_done", "total_frames",
        "output_path", "error", "config_json", "source_type",
        "source_file_id", "source_name", "target_type",
        "target_count", "target_summary"
    }
    
    set_clauses = []
    params = []
    for k, v in updates.items():
        if k in allowed_cols:
            set_clauses.append(f"{k} = ?")
            params.append(v)
            
    if not set_clauses:
        return False
        
    set_clauses.append("updated_at = CURRENT_TIMESTAMP")
    params.append(job_id)
    
    query = f"UPDATE jobs SET {', '.join(set_clauses)} WHERE id = ?"
    
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        affected = cursor.rowcount
        return affected > 0

def get_job_record(job_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single job by its ID."""
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def list_job_records(
    platform: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """Lists jobs with optional platform and status filters, ordered by newest first."""
    query = "SELECT * FROM jobs"
    conditions = []
    params = []
    
    if platform:
        conditions.append("platform = ?")
        params.append(platform)
        
    if status:
        if status in ["active", "ongoing"]:
            conditions.append("status IN ('pending', 'processing')")
        else:
            conditions.append("status = ?")
            params.append(status)
            
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

def get_jobs_count(platform: Optional[str] = None, status: Optional[str] = None) -> int:
    """Gets total count of jobs matching criteria."""
    query = "SELECT COUNT(*) FROM jobs"
    conditions = []
    params = []
    
    if platform:
        conditions.append("platform = ?")
        params.append(platform)
        
    if status:
        if status in ["active", "ongoing"]:
            conditions.append("status IN ('pending', 'processing')")
        else:
            conditions.append("status = ?")
            params.append(status)
            
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        return count

def get_active_jobs_count(platform: Optional[str] = None) -> int:
    """Returns number of pending or processing jobs."""
    return get_jobs_count(platform=platform, status="active")

def delete_job_record(job_id: str) -> bool:
    """Deletes a job from the database."""
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM jobs WHERE id = ?', (job_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected > 0

def clear_completed_job_records(platform: Optional[str] = None) -> int:
    """Deletes all completed, failed, or cancelled jobs."""
    query = "DELETE FROM jobs WHERE status IN ('completed', 'failed', 'cancelled')"
    params = []
    if platform:
        query += " AND platform = ?"
        params.append(platform)
        
    with _db_lock:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        affected = cursor.rowcount
        return affected

