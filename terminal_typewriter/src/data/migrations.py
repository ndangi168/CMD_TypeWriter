from .storage import StorageManager


def run_migrations(db_path: str | None = None) -> None:
    StorageManager(db_path=db_path)  # initialization ensures schema