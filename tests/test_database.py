from pathlib import Path
from datetime import datetime
from src.models.speed_event_model import SpeedEvent
from src.database import create_table, insert_event, get_all_events

TEST_DB = Path("tests/test_events.db")


def main():
    create_table(TEST_DB)

    events = [
        SpeedEvent(1, datetime.now(), 12.4, 15.0, None, "Test A"),
        SpeedEvent(2, datetime.now(), 18.7, 15.0, "img2.jpg", "Test B"),
    ]

    for event in events:
        insert_event(event, TEST_DB)

    saved = get_all_events(TEST_DB)

    for e in saved:
        print(e)


if __name__ == "__main__":
    main()