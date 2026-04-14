"""
Entry point for application.
Starts the radar, LCD, and camera services. Then runs the main monitoring loop.
"""

import time
from pathlib import Path

from src.config.settings import (
    MIN_VALID_SPEED_MPH,
    RADAR_POLL_INTERVAL_SECONDS,
    SPEED_THRESHOLD_MPH,
    CAPTURE_COOLDOWN_SECONDS,
    DEFAULT_LOCATION,
    BURST_CAPTURE_DURATION_SECONDS,
    BURST_CAPTURE_INTERVAL_SECONDS,
)
from src.display.lcd_display import LCDDisplay
from src.camera.capture import CameraCapture
from src.radar.radar import RadarSensor
from src.database import create_table
from src.logic.violation_handler import ViolationHandler


def main() -> None:
    lcd = LCDDisplay()
    radar = RadarSensor()
    camera = CameraCapture()
    violation_handler = ViolationHandler(
        threshold_mph=SPEED_THRESHOLD_MPH,
        location=DEFAULT_LOCATION,
    )

    last_capture_time = 0.0
    base_dir = Path(__file__).resolve().parent.parent
    captures_root = base_dir / "data" / "captures"

    try:
        lcd.show_startup()
        time.sleep(1)

        lcd.write_lines("Connecting...", "Radar USB")
        radar.connect()

        create_table()
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

            now = time.time()

            if not reading.detected or reading.speed_mph < MIN_VALID_SPEED_MPH:
                lcd.show_no_target()

            elif reading.speed_mph >= SPEED_THRESHOLD_MPH:
                lcd.show_warning(reading.speed_mph)

                if now - last_capture_time >= CAPTURE_COOLDOWN_SECONDS:
                    relative_image_paths = []

                    try:
                        image_paths = camera.capture_burst(
                            speed_mph=reading.speed_mph,
                            direction=reading.direction,
                            duration_seconds=BURST_CAPTURE_DURATION_SECONDS,
                            interval_seconds=BURST_CAPTURE_INTERVAL_SECONDS,
                        )

                        if image_paths:
                            relative_image_paths = [
                                str(Path(path).resolve().relative_to(captures_root.resolve()))
                                for path in image_paths
                            ]

                        print(f"Burst captured: {len(relative_image_paths)} images")
                        for relative_path in relative_image_paths:
                            print(f"  {relative_path}")

                    except Exception as camera_exc:
                        print(f"Burst capture failed: {camera_exc}")
                        lcd.show_error("Camera failed")

                    try:
                        event = violation_handler.save_event(
                            speed_mph=reading.speed_mph,
                            image_paths=relative_image_paths,
                        )
                        last_capture_time = now
                        print(
                            f"Violation event saved: "
                            f"{event.speed_mph:.2f} mph | "
                            f"{event.location} | "
                            f"{event.image_paths}"
                        )
                    except Exception as db_exc:
                        print(f"Failed to save event: {db_exc}")
                        lcd.show_error("DB save failed")

            else:
                lcd.show_speed(reading.speed_mph, reading.direction)

            time.sleep(RADAR_POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nStopped by user.")
        lcd.write_lines("Stopping...", "")
        time.sleep(1)
        lcd.show_idle()

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