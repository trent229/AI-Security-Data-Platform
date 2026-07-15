"""SQLite database setup for the AI Security Data Platform."""

import sqlite3
from pathlib import Path


DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
DATABASE_PATH = DATA_DIRECTORY / "security_events.db"


def get_connection() -> sqlite3.Connection:
    """Create and configure a connection to the security database."""
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the security-events table if it does not exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL DEFAULT 'info',
                description TEXT NOT NULL,
                confidence REAL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()