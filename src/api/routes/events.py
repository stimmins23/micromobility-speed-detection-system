"""

Event endpoints

"""

from fastapi import APIRouter
from src.api.schemas.event import Event

router = APIRouter()

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
    return sample_events