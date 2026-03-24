"""

Entry point for application. 
Starts the radar, LCD, and camera services. Then runs the main monitoring loop. 

"""

# Currently only testing LCD startup and idle messages

import time

from src.display.lcd_display import LCDDisplay

def main() -> None:
    lcd = LCDDisplay()
    lcd.show_startup()
    time.sleep(2)
    lcd.show_idle()


if __name__ == "__main__":
    main()