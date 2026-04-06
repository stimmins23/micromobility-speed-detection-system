from dataclasses import dataclass
from datetime import datetime

@dataclass
class SpeedEvent:
    id: int 
    timestamp: datetime 
    speed_mph: float 
    threshold_value: float 
    image_path: str | None # allows null images
    location: str

