from pathlib import Path
from src.database import get_all_events

TEST_DB = Path("tests/test_events.db")

events = get_all_events(TEST_DB)

print("\n=== EVENTS IN DATABASE ===\n")

for e in events:
    print(f"ID: {e.id}")
    print(f"Time: {e.timestamp}")
    print(f"Speed: {e.speed_mph} mph")
    print(f"Threshold: {e.threshold_value} mph")
    print(f"Image: {e.image_path}")
    print(f"Location: {e.location}")
    print("-" * 30)