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
        threshold_value=event.threshold_value,
        image_paths=event.image_paths,
        location=event.location,
    )


@router.get("/events", response_model=list[Event])
def get_events():
    events = get_all_events()
    return [to_event_schema(event) for event in events]