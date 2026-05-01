"""

Central application configuration.
Stores settings for radar UART connection, LCD display, camera settings, threshold behavior, file paths, and dashboard/backend settings. 

"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Radar / USB settings
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 38400
SERIAL_TIMEOUT = 1.0
RADAR_POLL_INTERVAL_SECONDS = 0.3    # radar polling


# LDC Settings
LCD_I2C_ADDRESS = 0x27
LCD_COLS = 16
LCD_ROWS = 2

# Speed threshold settings
SPEED_THRESHOLD_MPH = 1.2
MIN_VALID_SPEED_MPH = 0.4
CAPTURE_COOLDOWN_SECONDS = 1.0
BURST_CAPTURE_DURATION_SECONDS = 1.0
BURST_CAPTURE_INTERVAL_SECONDS = 0.05
WARNING_DISPLAY_SECONDS = 1.5
DEFAULT_LOCATION = "Miracle Mile, Coral Gables"

# Speed conversions - update later when confirm exact S04/Sample rate setting and conversion
BIN_TO_MPH_FACTOR = 0.14

# Storage paths
DATA_DIR = BASE_DIR / "data"
CAPTURE_DIR = DATA_DIR / "captures"
LOG_DIR = DATA_DIR / "logs"
DB_PATH = DATA_DIR / "events.db" 

# Dashboard settings
API_HOST= "0.0.0.0"
API_PORT = 8000

