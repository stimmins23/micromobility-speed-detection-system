"""

Central application configuration.
Stores settings for radar UART connection, LCD display, camera settings, threshold behavior, file paths, and dashboard/backend settings. 

"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Radar / UART settings
SERIAL_PORT = "/dev/serial0"
BAUD_RATE = 38400
SERIAL_TIMEOUT = 1.0

# LDC Settings
LCD_I2C_ADDRESS = 0x27
LCD_COLS = 16
LCD_ROWS = 2

# Speed threshold settings
SPEED_THRESHOLD_MPH = 15
MIN_VALID_SPEED_MPH = 3
CAPTURE_COOLDOWN_SECONDS = 5
WARNING_DISPLAY_SECONDS = 2

# Storage paths
DATA_DIR = BASE_DIR / "data"
CAPTURE_DIR = DATA_DIR / "captures"
LOG_DIR = DATA_DIR / "logs"
DB_DIR = DATA_DIR / "db" 

# Dashboard settings
API_HOST= "0.0.0.0"
API_PORT = 8000

