"""

Radar device interface.
Handles USB serial communication with radar sensor and provides helper. Methods for sending commands and retrieving parsed target data.

"""

from __future__ import annotations

import serial

from src.config.settings import SERIAL_PORT,BAUD_RATE, SERIAL_TIMEOUT
from src.radar.parser import RadarReading, parse_c00_response

class RadarSensor:
    def __init__(self):
        self.serial_port = SERIAL_PORT
        self.baud_rate = BAUD_RATE
        self.timeout = SERIAL_TIMEOUT
        self.connection: serial.Serial | None = None

    
    def connect(self) -> None:
        self.connection = serial.Serial(
            port=self.serial_port,
            baudrate=self.baud_rate,
            timeout=self.timeout,
        )

    def disconnect(self) -> None:
        if self.connection and self.connection.is_open:
            self.connection.close()

    def is_connected(self) -> None:
        return self.connection is not None and self.connection.is_open

    def read_line(self) -> bytes:
        if not self.is_connected():
            raise RuntimeError("Radar serial connection is not open.")
        return self.connection.readline()
    
    def read_bytes(self, size: int = 128) -> bytes:
        if not self.is_connected():
            raise RuntimeError("Radial serial connection is not open.")
        return self.connection.readline()
        
    def write_bytes(self, data: bytes) -> None:
        if not self.is_connected():
            raise RuntimeError("Radar serial connection is not open.")
        self.connection.write(data)

    def send_command(self, command: str) -> str:
        """
        Send ASCII radar command and return deconded response string.

        """
        if not command.endswith("\r"):
            command += "\r"

        self.write_bytes(command.encode("ascii"))
        response = self.read_line()
        return response.decode("ascii", errors="ignore").strip()
    
    def get_device_type(self) -> str:
        return self.send_command("$F01")
    
    def get_firmware_version(self) -> str:
        return self.send_command("$F00")
    
    def get_target_string(self) -> str:
        return self.send_command("$C00")
    
    def get_target_data(self) -> RadarReading | None:
        raw_response = self.get_target_string()
        if not raw_response:
            return None
        return parse_c00_response(raw_response)