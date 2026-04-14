"""

Event endpoints

"""

from fastapi import APIRouter
from src.api.schemas.event import Event
from src.database import get_all_events
from src.models.speed_event_model import SpeedEvent

router = APIRouter()

def to_event_schema(event: SpeedEvent) -> Event:
    return Event(
        id=event.id,
        timestamp=event.timestamp.isoformat(),
        speed_mph=event.speed_mph,
        threshold_value=event.threshold.value,
        image_path=event.image_path,
        location=event.location,
    )

sample_events = [
    Event(
        id=1,
        timestamp="2026-04-10T09:15:00",
        speed_mph=18.4,
        threshold_value=15.0,
        image_path="images/event1.jpg",
        location="Ponce de Leon Blvd"
    ),
    Event(
        id=2,
        timestamp="2026-04-10T09:22:00",
        speed_mph=21.7,
        threshold_value=15.0,
        image_path="images/event2.jpg",
        location="Miracle Mile"
    ),
    Event(
        id=3,
        timestamp="2026-04-10T09:40:00",
        speed_mph=14.2,
        threshold_value=15.0,
        image_path=None,
        location="Test Location A"
    )
]

@router.get("/events", response_model=list[Event])
def get_events():
    events = get_all_events()
    return [to_event_schema(event) for event in events]