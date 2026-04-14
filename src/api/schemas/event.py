"""
Request / response models
"""

from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    id: int
    timestamp: str
    speed_mph: float
    threshold_value: float
    image_path: Optional[str] = None
    location: str