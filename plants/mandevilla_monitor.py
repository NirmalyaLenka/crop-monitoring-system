"""
Greenhouse monitor for Mandevilla (a flowering tropical vine).

The ranges below reflect typical Mandevilla care guidance: warm days,
mild nights with real cold sensitivity below about 10 C, moderate
humidity, strong light, and soil kept lightly moist but never soggy.
See docs/plant-profiles.md for full research notes, sources, and
precautions specific to Mandevilla.

Before running this script:
    1. Copy config/settings_example.py to config/settings.py and fill
       in your email/SMS details (see docs/alerts-setup.md).
    2. Wire up the sensors as described in docs/hardware-setup.md.
    3. Calibrate the soil moisture sensor as described in
       docs/hardware-setup.md.

Run with (from the repository root folder):
    python3 plants/mandevilla_monitor.py
Stop with Ctrl+C
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core import engine

PROFILE = {
    "name": "Mandevilla",
    "temperature_c": (15, 32),         # cold damage risk below about 10 C
    "humidity_percent": (50, 60),
    "soil_moisture_percent": (45, 70),   # lightly moist, allow the top layer to dry between waterings
    "light_lux": (8000, 130000),         # at least 6 hours of bright light, tolerates some partial shade
    "air_quality_raw_max": 30000,        # general air freshness check, calibrate to your own baseline, see docs/hardware-setup.md
    "notes": (
        "Mandevilla is a tropical vine that is sensitive to cold, "
        "so protect it well below 10 C. It flowers best with strong "
        "light and dislikes sitting in soggy soil."
    ),
}

if __name__ == "__main__":
    engine.run_monitor(PROFILE)
