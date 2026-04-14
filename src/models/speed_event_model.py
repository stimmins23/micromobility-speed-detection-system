from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SpeedEvent:
    id: int | None = None
    timestamp: datetime | None = None
    speed_mph: float = 0.0
    threshold_value: float = 0.0
    image_paths: list[str] = field(default_factory=list)
    location: str = ""