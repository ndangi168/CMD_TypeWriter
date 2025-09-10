import json
import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, Optional, List

from ..utils.exceptions import StorageException


DB_RELATIVE_PATH = os.path.join("terminal_typewriter", "data", "database", "typewriter.db")


def ensure_directory(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


class StorageManager:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or os.path.join(os.getcwd(), DB_RELATIVE_PATH)
        ensure_directory(self.db_path)
        self._init_db()

    @contextmanager
    def _connect(self):
        try:
            conn = sqlite3.connect(self.db_path)
            yield conn
            conn.close()
        except Exception as exc:
            raise StorageException(str(exc))

    def _init_db(self) -> None:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    mode TEXT,
                    duration REAL,
                    text_length INTEGER,
                    wpm REAL,
                    accuracy REAL,
                    errors INTEGER,
                    keystrokes_data TEXT
                )
                """
            )
            conn.commit()

    def save_session(self, session: Dict[str, Any]) -> None:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO sessions (id, timestamp, mode, duration, text_length, wpm, accuracy, errors, keystrokes_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session["id"],
                    session.get("timestamp"),
                    session.get("mode"),
                    session.get("duration"),
                    session.get("text_length"),
                    session.get("wpm"),
                    session.get("accuracy"),
                    session.get("errors"),
                    json.dumps(session.get("keystrokes", [])),
                ),
            )
            conn.commit()

    def fetch_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, timestamp, mode, duration, text_length, wpm, accuracy, errors
                FROM sessions
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = cur.fetchall()
            return [
                {
                    "id": r[0],
                    "timestamp": r[1],
                    "mode": r[2],
                    "duration": r[3],
                    "text_length": r[4],
                    "wpm": r[5],
                    "accuracy": r[6],
                    "errors": r[7],
                }
                for r in rows
            ]

    def count_sessions(self) -> int:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(1) FROM sessions")
            (count,) = cur.fetchone()
            return int(count)

    def fetch_latest_session_with_keystrokes(self) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, timestamp, mode, duration, text_length, wpm, accuracy, errors, keystrokes_data
                FROM sessions
                ORDER BY timestamp DESC
                LIMIT 1
                """
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "id": row[0],
                "timestamp": row[1],
                "mode": row[2],
                "duration": row[3],
                "text_length": row[4],
                "wpm": row[5],
                "accuracy": row[6],
                "errors": row[7],
                "keystrokes": json.loads(row[8] or "[]"),
            }

    def fetch_session_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, timestamp, mode, duration, text_length, wpm, accuracy, errors, keystrokes_data
                FROM sessions
                WHERE id = ?
                LIMIT 1
                """,
                (session_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "id": row[0],
                "timestamp": row[1],
                "mode": row[2],
                "duration": row[3],
                "text_length": row[4],
                "wpm": row[5],
                "accuracy": row[6],
                "errors": row[7],
                "keystrokes": json.loads(row[8] or "[]"),
            }