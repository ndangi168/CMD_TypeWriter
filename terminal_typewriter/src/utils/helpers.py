import uuid
from datetime import datetime


def generate_session_id() -> str:
    return str(uuid.uuid4())


def now_utc_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"