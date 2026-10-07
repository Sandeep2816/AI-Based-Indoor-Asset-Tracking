import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "asset_tracking.db")

@contextmanager
def connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            tag_id TEXT NOT NULL,
            anchor_id TEXT NOT NULL,
            rssi REAL NOT NULL
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            tag_id TEXT NOT NULL,
            x REAL NOT NULL,
            y REAL NOT NULL,
            method TEXT NOT NULL
        )
        """)

def save_observation(timestamp, tag_id, anchor_id, rssi):
    with connection() as conn:
        conn.execute(
            "INSERT INTO observations(timestamp,tag_id,anchor_id,rssi) VALUES(?,?,?,?)",
            (timestamp, tag_id, anchor_id, rssi)
        )

def save_position(timestamp, tag_id, x, y, method):
    with connection() as conn:
        conn.execute(
            "INSERT INTO positions(timestamp,tag_id,x,y,method) VALUES(?,?,?,?,?)",
            (timestamp, tag_id, x, y, method)
        )

def history(tag_id=None, limit=100):
    with connection() as conn:
        if tag_id:
            rows=conn.execute(
                "SELECT timestamp,tag_id,x,y,method FROM positions WHERE tag_id=? ORDER BY timestamp DESC LIMIT ?",
                (tag_id, limit)
            ).fetchall()
        else:
            rows=conn.execute(
                "SELECT timestamp,tag_id,x,y,method FROM positions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [dict(r) for r in rows]
