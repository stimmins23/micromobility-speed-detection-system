from dataclasses import dataclass
from datetime import datetime
from typing import Optional
<<<<<<< HEAD


@dataclass
class SpeedEvent:
    id: Optional[int]
    timestamp: datetime
    speed_mph: float
    threshold_value: float
    image_path: Optional[str]
    location: str
=======

@dataclass
class SpeedEvent:
    id: int 
    timestamp: datetime 
    speed_mph: float 
    threshold_value: float 
    image_path: Optional[str]
    location: str

>>>>>>> 75f5325e05d17dc3b872a470d28561c670910056
