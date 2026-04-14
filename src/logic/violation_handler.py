from datetime import datetime

from src.database import insert_event
from src.models.speed_event_model import SpeedEvent


class ViolationHandler:
    def __init__(self, threshold_mph: float, location: str) -> None:
        self.threshold_mph = threshold_mph
        self.location = location

    def create_event(
        self,
        speed_mph: float,
        image_paths: list[str] | None,
    ) -> SpeedEvent:
        return SpeedEvent(
            id=None,
            timestamp=datetime.now(),
            speed_mph=speed_mph,
            threshold_value=self.threshold_mph,
            image_paths=image_paths or [],
            location=self.location,
        )

    def save_event(
        self,
        speed_mph: float,
        image_paths: list[str] | None,
    ) -> SpeedEvent:
        event = self.create_event(
            speed_mph=speed_mph,
            image_paths=image_paths,
        )
        return insert_event(event)