import json
import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict

from ..utils.exceptions import StorageException


DB_RELATIVE_PATH = os.path.join("terminal_typewriter", "data", "database", "typewriter.db")


def ensure_directory(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


class StorageManager:
    def __init__(self, db_path: str | None = None) -> None:
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