"""
Greenhouse monitor for citrus trees (for example lemon, orange, lime).

The ranges below reflect typical greenhouse citrus guidance: warm days,
frost-free nights, moderate humidity, strong light, and soil allowed to
dry slightly between waterings. See docs/plant-profiles.md for full
research notes, sources, and precautions specific to citrus.

Before running this script:
    1. Copy config/settings_example.py to config/settings.py and fill
       in your email/SMS details (see docs/alerts-setup.md).
    2. Wire up the sensors as described in docs/hardware-setup.md.
    3. Calibrate the soil moisture sensor as described in
       docs/hardware-setup.md.

Run with (from the repository root folder):
    python3 plants/citrus_monitor.py
Stop with Ctrl+C
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core import engine

PROFILE = {
    "name": "Citrus",
    "temperature_c": (10, 29),        # growth stalls below 10 C, frost risk below about 4 C
    "humidity_percent": (50, 60),
    "soil_moisture_percent": (35, 65),  # allow the top layer to dry between waterings
    "light_lux": (8000, 130000),        # at least 6-8 hours of strong light daily
    "air_quality_raw_max": 30000,       # general air freshness check, calibrate to your own baseline, see docs/hardware-setup.md
    "notes": (
        "Citrus trees are frost-sensitive and stop growing in cold "
        "conditions, so protect them well below 10 C. They prefer "
        "their soil to dry out somewhat between waterings rather than "
        "staying constantly wet, which can cause root rot."
    ),
}

if __name__ == "__main__":
    engine.run_monitor(PROFILE)
