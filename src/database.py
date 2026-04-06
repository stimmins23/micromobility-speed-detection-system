import sqlite3
from pathlib import Path
from datetime import datetime
from src.models.speed_event_model import SpeedEvent

DEFAULT_DB_PATH = Path("data/events.db")


def get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def create_table(db_path: Path = DEFAULT_DB_PATH) -> None:
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                speed_mph REAL NOT NULL,
                threshold_value REAL NOT NULL,
                image_path TEXT,
                location TEXT NOT NULL
            )
            """
        )
        conn.commit()


def insert_event(event: SpeedEvent, db_path: Path = DEFAULT_DB_PATH) -> None:
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO events (
                timestamp,
                speed_mph,
                threshold_value,
                image_path,
                location
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event.timestamp.isoformat(),
                event.speed_mph,
                event.threshold_value,
                event.image_path,
                event.location,
            ),
        )
        conn.commit()


def get_all_events(db_path: Path = DEFAULT_DB_PATH) -> list[SpeedEvent]:
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, timestamp, speed_mph, threshold_value, image_path, location
            FROM events
            ORDER BY id
            """
        )
        rows = cursor.fetchall()

    events = []
    for row in rows:
        events.append(
            SpeedEvent(
                id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                speed_mph=row[2],
                threshold_value=row[3],
                image_path=row[4],
                location=row[5],
            )
        )
    return events