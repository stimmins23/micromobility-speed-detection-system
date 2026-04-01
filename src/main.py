"""

Entry point for application. 
Starts the radar, LCD, and camera services. Then runs the main monitoring loop. 

"""

# Currently only testing LCD startup and idle messages

import time

from src.config.settings import (
    MIN_VALID_SPEED_MPH,
    RADAR_POLL_INTERVAL_SECONDS,
    SPEED_THRESHOLD_MPH,
    CAPTURE_COOLDOWN_SECONDS,
)

from src.display.lcd_display import LCDDisplay
from src.camera.capture import CameraCapture
from src.radar.radar import RadarSensor


def main() -> None:
    lcd = LCDDisplay()
    radar = RadarSensor()
    camera = CameraCapture()

    last_capture_time = 0.0

    try: 
        lcd.show_startup()
        time.sleep(1)

        lcd.write_lines("Connecting...", "Radar USB")
        radar.connect()

        camera.start()

        device_type = radar.get_device_type()
        firmware = radar.get_firmware_version()

        print(f"Device type response: {device_type}")
        print(f"Firmware response: {firmware}")

        lcd.write_lines("Radar Connected", "Check Terminal")
        time.sleep(1)

        lcd.show_idle()
        time.sleep(1)

        while True:
            reading = radar.get_target_data()

            if reading is None:
                print("Could not parse C00 response.")
                lcd.show_error("Parse failed")
                time.sleep(RADAR_POLL_INTERVAL_SECONDS)
                continue

            print(
                f"detected={reading.detected} | "
                f"direction={reading.direction} | "
                f"speed_bin={reading.speed_bin} | "
                f"speed_mph={reading.speed_mph:.2f} | "
                f"magnitude_db={reading.magnitude_db} | "
                f"raw={reading.raw_response} | "    
            )


            if not reading.detected or reading.speed_mph < MIN_VALID_SPEED_MPH:
                lcd.show_no_target()

            elif reading.speed_mph >= SPEED_THRESHOLD_MPH:
                lcd.show_warning(reading.speed_mph)

                now = time.time()
                if now - last_capture_time >= CAPTURE_COOLDOWN_SECONDS:
                    try:
                        image_path = camera.capture_image(
                            speed_mph=reading.speed_mph,
                            direction=reading.direction,
                        )
                        last_capture_time = now
                        print(f"Image captured: {image_path}")
                    except Exception as camera_exc:
                        print(f"Camera capture failed: {camera_exc}")
                        lcd.show_error("Camera failed")

            else:
                lcd.show_speed(reading.speed_mph, reading.direction)

            time.sleep(RADAR_POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nStopped by user.")
        lcd.write_lines("Stopping...", "")
        time.sleep(1)
        lcd.show_idle

    except Exception as exc:
        print(f"Radar test error: {exc}")
        lcd.write_lines("Radar Error", str(exc)[:16])
        time.sleep(3)


    finally:
        try:
            radar.disconnect()
        except Exception:
            pass

        try:
            camera.stop()
        except Exception:
            pass

        try:
            lcd.clear()
        except Exception:
            pass


if __name__ == "__main__":
    main()