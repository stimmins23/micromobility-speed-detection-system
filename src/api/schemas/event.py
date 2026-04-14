from pydantic import BaseModel


class Event(BaseModel):
    id: int
    timestamp: str
    speed_mph: float
    threshold_value: float
    image_paths: list[str]
    location: str