import os
import tempfile

from src.data.storage import StorageManager


def test_storage_save_and_fetch_latest():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "typewriter.db")
        storage = StorageManager(db_path=db_path)

        session = {
            "id": "test-1",
            "timestamp": "2024-01-01T00:00:00Z",
            "mode": "beginner",
            "duration": 30.0,
            "text_length": 100,
            "wpm": 50.0,
            "accuracy": 95.0,
            "errors": 3,
            "keystrokes": [{"t": 0.1, "k": "a"}],
            "text": "hello world",
        }
        storage.save_session(session)

        fetched = storage.fetch_latest_session_with_keystrokes()
        assert fetched is not None
        assert fetched["id"] == session["id"]
        assert fetched["text"] == session["text"]
        assert isinstance(fetched["keystrokes"], list)