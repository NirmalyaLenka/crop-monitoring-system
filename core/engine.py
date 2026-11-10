"""
Shared monitoring loop used by every plant script in this repository.

Each script in the plants folder defines a PROFILE dictionary
describing that plant's ideal sensor ranges, then calls
run_monitor(profile). All the shared logic (reading sensors, logging
data, taking photos, checking thresholds, and sending alerts) lives
here, so that adding a new plant only means writing a new profile,
not new monitoring code.
"""

from datetime import datetime
import json
import os
import time

from config import settings
from core import alerts, camera_capture, data_logger, sensors


def _check_range(value, value_range, label, unit=""):
    """
    Returns a warning string if value falls outside value_range (a
    (min, max) tuple), or None if the value is within range or missing.
    """
    if value is None or value_range is None:
        return None

    minimum, maximum = value_range
    if value < minimum:
        return f"{label} is too LOW: {value}{unit} (expected {minimum} to {maximum}{unit})"
    if value > maximum:
        return f"{label} is too HIGH: {value}{unit} (expected {minimum} to {maximum}{unit})"
    return None


def _find_latest_photo(photos_dir):
    if not os.path.isdir(photos_dir):
        return None
    photos = sorted(os.listdir(photos_dir))
    return photos[-1] if photos else None


def run_monitor(profile):
    plant_name = profile["name"]
    plant_slug = plant_name.lower()
    data_dir = settings.DATA_DIR
    csv_path = os.path.join(data_dir, f"{plant_slug}_log.csv")
    photos_dir = os.path.join(data_dir, "photos", plant_slug)
    state_path = os.path.join(data_dir, f"{plant_slug}_state.json")

    fieldnames = [
        "timestamp", "temperature_c", "humidity_percent", "light_lux",
        "soil_moisture_percent", "air_quality_raw", "air_quality_voltage",
        "status",
    ]

    print(f"Starting greenhouse monitor for: {plant_name}")
    print("Logging to:", csv_path)
    print("Photos saved to:", photos_dir)
    print("Dashboard (run separately): python3 core/dashboard.py")
    print("Press Ctrl+C to stop.\n")

    last_photo_time = None

    try:
        while True:
            reading = sensors.read_all()
            timestamp = datetime.now().isoformat(timespec="seconds")

            warnings = [
                _check_range(reading["temperature_c"], profile.get("temperature_c"), "Temperature", " C"),
                _check_range(reading["humidity_percent"], profile.get("humidity_percent"), "Humidity", "%"),
                _check_range(reading["soil_moisture_percent"], profile.get("soil_moisture_percent"), "Soil/substrate moisture", "%"),
                _check_range(reading["light_lux"], profile.get("light_lux"), "Light level", " lux"),
            ]

            air_quality_max = profile.get("air_quality_raw_max")
            if air_quality_max is not None and reading["air_quality_raw"] is not None:
                if reading["air_quality_raw"] > air_quality_max:
                    warnings.append(
                        f"Air quality reading is high: {reading['air_quality_raw']} "
                        f"(expected below {air_quality_max}, calibrate this in docs/hardware-setup.md)"
                    )

            warnings = [w for w in warnings if w]
            status = "normal" if not warnings else "ALERT"

            row = {
                "timestamp": timestamp,
                "temperature_c": reading["temperature_c"],
                "humidity_percent": reading["humidity_percent"],
                "light_lux": reading["light_lux"],
                "soil_moisture_percent": reading["soil_moisture_percent"],
                "air_quality_raw": reading["air_quality_raw"],
                "air_quality_voltage": reading["air_quality_voltage"],
                "status": status,
            }
            data_logger.log_row(csv_path, fieldnames, row)

            new_photo = None
            now = datetime.now()
            if (
                last_photo_time is None
                or (now - last_photo_time).total_seconds() >= settings.PHOTO_INTERVAL_MINUTES * 60
            ):
                new_photo = camera_capture.capture_photo(photos_dir)
                camera_capture.clean_old_photos(photos_dir, settings.PHOTO_RETENTION_DAYS)
                last_photo_time = now

            latest_photo = new_photo or _find_latest_photo(photos_dir)

            state = {
                "plant_name": plant_name,
                "timestamp": timestamp,
                "reading": reading,
                "status": status,
                "warnings": warnings,
                "latest_photo": latest_photo,
            }
            os.makedirs(data_dir, exist_ok=True)
            with open(state_path, "w") as f:
                json.dump(state, f)

            print(timestamp, "-", status, "-", reading)

            if warnings:
                photo_path = os.path.join(photos_dir, latest_photo) if latest_photo else None
                subject = f"Greenhouse alert: {plant_name}"
                body = (
                    f"{plant_name} monitor detected the following at {timestamp}:\n\n"
                    + "\n".join(warnings)
                )
                alerts.send_alert_if_needed(plant_name, subject, body, photo_path)

            time.sleep(settings.READING_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nStopped by user")
