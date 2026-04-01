"""
Camera capture helper using Picamera2.
"""

from datetime import datetime
from pathlib import Path
import time

from picamera2 import Picamera2

from libcamera import Transform

from src.config.settings import CAPTURE_DIR


class CameraCapture:
    def __init__(self) -> None:
        self.camera = Picamera2()
        self.started = False

        Path(CAPTURE_DIR).mkdir(parents=True, exist_ok=True)

    def start(self) -> None:
        if self.started:
            return

        config = self.camera.create_still_configuration(
            transform=Transform(hflip=True, vflip= True) # 180 degree rotation
        )
        
        self.camera.configure(config)
        self.camera.start()
        time.sleep(1)
        self.started = True

    def stop(self) -> None:
        if self.started:
            self.camera.stop()
            self.started = False

    def capture_image(self, speed_mph: float, direction: str = "") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_direction = direction.lower() if direction else "unknown"

        filename = f"{timestamp}_{speed_mph:.1f}mph_{safe_direction}.jpg"
        filepath = Path(CAPTURE_DIR) / filename

        self.camera.capture_file(str(filepath))
        return str(filepath)