"""

LCD interface module.
Sends status messages and speed warnings to the I2C LCD screen.

"""

from RPLCD.i2c import CharLCD

from src.config.settings import LCD_I2C_ADDRESS, LCD_COLS, LCD_ROWS

class LCDDisplay:
    def __init__(self) -> None:
        self.lcd = CharLCD(
            i2c_expander="PCF8574",
            address=LCD_I2C_ADDRESS,
            port=1,
            cols=LCD_COLS,
            rows=LCD_ROWS,
            charmap="A02",
            auto_linebreaks=False,
        )

    def clear(self) -> None:
        self.lcd.clear()

    def write_lines(self, line1: str = "", line2: str = "") -> None:
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(line1[:LCD_COLS].ljust(LCD_COLS))
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(line2[:LCD_COLS].ljust(LCD_COLS))

    def show_startup(self) -> None:
        self.write_lines("Radar Starting", "Please wait...")

    def show_idle(self) -> None:
        self.write_lines("Radar Ready", "Waiting...")

    def show_speed(self, speed_mph: float, direction: str) -> None:
        short_dir = "Approach" if direction == "approaching" else "Recede"
        self.write_lines(f"Speed {speed_mph:.1f}", short_dir)

    def show_warning(self, speed_mph: float) -> None:
        self.write_lines(f"Speed {speed_mph}:.1f", " SLOW DOWN!")

    def show_no_target(self) -> None:
        self.write_lines("No Target", "Monitoring...")

    def show_error(self, message: str) -> None:
        self.write_lines("Radar Error", message[:16])