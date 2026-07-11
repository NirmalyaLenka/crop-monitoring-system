"""
Camera capture and photo storage management for the greenhouse
monitoring system.

Uses Picamera2, which works on Raspberry Pi 3, Pi 4, and Pi 5. See the
separate raspberry-pi-camera-guide project for full camera wiring and
setup instructions, since the camera connector differs between Pi 3/4
and Pi 5.

Install first if needed:
    sudo apt install -y python3-picamera2
"""

import os
import time
from datetime import datetime, timedelta

from picamera2 import Picamera2

_picam2 = None


def _get_camera():
    global _picam2
    if _picam2 is None:
        _picam2 = Picamera2()
        config = _picam2.create_still_configuration()
        _picam2.configure(config)
        _picam2.start()
        time.sleep(2)
    return _picam2


def capture_photo(photos_dir):
    """
    Captures a single timestamped photo into photos_dir.
    Returns the filename (not the full path) of the saved photo, or
    None if the capture failed.
    """
    os.makedirs(photos_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.jpg"
    filepath = os.path.join(photos_dir, filename)

    try:
        camera = _get_camera()
        camera.capture_file(filepath)
        return filename
    except Exception as error:
        print("Camera capture failed:", error)
        return None


def clean_old_photos(photos_dir, retention_days):
    """
    Deletes photos older than retention_days from photos_dir, so a
    long-running greenhouse setup does not slowly fill up the SD card.
    """
    if not os.path.isdir(photos_dir):
        return

    cutoff = datetime.now() - timedelta(days=retention_days)

    for filename in os.listdir(photos_dir):
        filepath = os.path.join(photos_dir, filename)
        try:
            modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if modified_time < cutoff:
                os.remove(filepath)
        except OSError:
            continue
