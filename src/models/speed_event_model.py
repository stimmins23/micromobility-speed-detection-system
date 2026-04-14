from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SpeedEvent:
    id: Optional[int]
    timestamp: datetime
    speed_mph: float
    threshold_value: float
    image_path: Optional[str]
    location: str
