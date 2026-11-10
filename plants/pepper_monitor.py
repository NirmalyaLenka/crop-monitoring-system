"""
Greenhouse monitor for pepper plants (bell pepper or chili pepper).

The ranges below reflect typical greenhouse pepper guidance: warm days,
mild nights, moderate humidity, and consistently moist (not soggy)
soil. See docs/plant-profiles.md for full research notes, sources, and
precautions specific to peppers.

Before running this script:
    1. Copy config/settings_example.py to config/settings.py and fill
       in your email/SMS details (see docs/alerts-setup.md).
    2. Wire up the sensors as described in docs/hardware-setup.md.
    3. Calibrate the soil moisture sensor as described in
       docs/hardware-setup.md.

Run with (from the repository root folder):
    python3 plants/pepper_monitor.py
Stop with Ctrl+C
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core import engine

PROFILE = {
    "name": "Pepper",
    "temperature_c": (15, 27),        # combined day (21-27) and night (15-21) band
    "humidity_percent": (50, 70),
    "soil_moisture_percent": (55, 75),  # consistently moist, never soggy
    "light_lux": (10000, 130000),       # at least 6 hours of direct light daily
    "air_quality_raw_max": 30000,       # general air freshness check, calibrate to your own baseline, see docs/hardware-setup.md
    "notes": (
        "Peppers like warm, consistent conditions and steady soil "
        "moisture. Avoid wetting the foliage directly when watering, "
        "since that encourages fungal disease in humid conditions."
    ),
}

if __name__ == "__main__":
    engine.run_monitor(PROFILE)
