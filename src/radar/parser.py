"""

Radar response parsing utilities.

Converts raw radar command responses to structured Python data that is usable by the LCD, threshold logic, camera trigger, and dashboard.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.config.settings import BIN_TO_MPH_FACTOR

@dataclass
class RadarReading:
    detected: bool
    direction: str
    speed_bin: int
    speed_mph: float
    magnitude_db: int
    raw_response: str


def _clean_response(raw_response: str) -> str:
    """
    Normalizing raw radar response into readable string.

    Examples or raw data:
        '@001;076;067'
        '001;076,067'
        '@C00;001;076;067'

    """

    text = raw_response.strip()

    if text.startswith("@"):
        text= text[1:]

    return text.strip()


def _extract_numeric_parts(cleaned_response: str) -> list[int]:
    """
    Extracts numeric chunks from semicolon-separated response.

    Makes parser more tolerant of optional prefixes like 'C00'.
    """

    parts = [part.strip() for part in cleaned_response.split(";") if part.strip()]
    numeric_parts: list[int] = []

    for part in parts:
        if part.isdigit():
            numeric_parts.append(int(part))

    return numeric_parts

def decode_detection_register(register_value: int) -> tuple[bool, str]:
    """
    Decode the detection register:
    - bit 0: detection flag
    - bit 1: direction flag

    """

    detected = bool(register_value & 0b0001)
    direction_bit = bool(register_value & 0b0010)

    direction = "approaching" if direction_bit else "receding"
    return detected, direction

def convert_bin_to_mph(speed_bin: int) -> float:
    """
    Convert radar speed bin into a provisional mph value.

    This factor needs to be updated later for the module's exact sampling configuration confirmed.

    """

    return round(speed_bin * BIN_TO_MPH_FACTOR, 2)

def parse_c00_response(raw_response: str) -> Optional[RadarReading]:
    """
    Parse a C00 resopnse into a RadarReading object. 

    Expected useful fields: detection register, speed bin, and magnitude dB

    Returns None if response cant be parsed

    """

    cleaned = _clean_response(raw_response)
    numeric_parts = _extract_numeric_parts(cleaned)

    if len(numeric_parts) < 3:
        return None
    
    detection_register = numeric_parts[0]
    speed_bin = numeric_parts[1]
    magnitude_db = numeric_parts[2]

    detected, direction = decode_detection_register(detection_register)
    speed_mph = convert_bin_to_mph(speed_bin)

    return RadarReading(
        detected=detected,
        direction=direction,
        speed_bin=speed_bin,
        speed_mph=speed_mph,
        magnitude_db=magnitude_db,
        raw_response=raw_response.strip()
    )

