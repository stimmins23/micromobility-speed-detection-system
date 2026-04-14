import json
import sqlite3
from pathlib import Path
from datetime import datetime

from src.config.settings import DB_PATH
from src.models.speed_event_model import SpeedEvent

DEFAULT_DB_PATH = DB_PATH


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
                image_paths TEXT,
                location TEXT NOT NULL
            )
            """
        )
        conn.commit()


def insert_event(event: SpeedEvent, db_path: Path = DEFAULT_DB_PATH) -> SpeedEvent:
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO events (
                timestamp,
                speed_mph,
                threshold_value,
                image_paths,
                location
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event.timestamp.isoformat() if event.timestamp else datetime.now().isoformat(),
                event.speed_mph,
                event.threshold_value,
                json.dumps(event.image_paths),
                event.location,
            ),
        )
        conn.commit()
        event.id = cursor.lastrowid
        return event


def get_all_events(db_path: Path = DEFAULT_DB_PATH) -> list[SpeedEvent]:
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, timestamp, speed_mph, threshold_value, image_paths, location
            FROM events
            ORDER BY id DESC
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
                image_paths=json.loads(row[4]) if row[4] else [],
                location=row[5],
            )
        )
    return events


def get_events_above_threshold(db_path: Path = DEFAULT_DB_PATH) -> list[SpeedEvent]:
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, timestamp, speed_mph, threshold_value, image_paths, location
            FROM events
            WHERE speed_mph >= threshold_value
            ORDER BY id
            """
        )
        rows = cursor.fetchall()

    return [
        SpeedEvent(
            id=row[0],
            timestamp=datetime.fromisoformat(row[1]),
            speed_mph=row[2],
            threshold_value=row[3],
            image_paths=json.loads(row[4]) if row[4] else [],
            location=row[5],
        )
        for row in rows
    ]


def get_events_above_speed(
    min_speed: float,
    db_path: Path = DEFAULT_DB_PATH,
) -> list[SpeedEvent]:
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, timestamp, speed_mph, threshold_value, image_paths, location
            FROM events
            WHERE speed_mph >= ?
            ORDER BY id
            """,
            (min_speed,),
        )
        rows = cursor.fetchall()

    return [
        SpeedEvent(
            id=row[0],
            timestamp=datetime.fromisoformat(row[1]),
            speed_mph=row[2],
            threshold_value=row[3],
            image_paths=json.loads(row[4]) if row[4] else [],
            location=row[5],
        )
        for row in rows
    ]


def get_events_by_location(
    location: str,
    db_path: Path = DEFAULT_DB_PATH,
) -> list[SpeedEvent]:
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, timestamp, speed_mph, threshold_value, image_paths, location
            FROM events
            WHERE location = ?
            ORDER BY id
            """,
            (location,),
        )
        rows = cursor.fetchall()

    return [
        SpeedEvent(
            id=row[0],
            timestamp=datetime.fromisoformat(row[1]),
            speed_mph=row[2],
            threshold_value=row[3],
            image_paths=json.loads(row[4]) if row[4] else [],
            location=row[5],
        )
        for row in rows
    ]