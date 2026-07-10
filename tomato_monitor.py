"""
Greenhouse monitor for tomato plants.

The ranges below reflect typical greenhouse tomato guidance: warm days,
cooler nights, moderate humidity to avoid fungal disease, and evenly
moist (never soggy) soil. See docs/plant-profiles.md for full research
notes, sources, and precautions specific to tomatoes.

Note: the temperature range below combines both day and night targets
into one simplified band, since this is a beginner monitoring project
rather than a full climate control system. See docs/plant-profiles.md
for the separate day/night figures if you want to fine-tune further.

Before running this script:
    1. Copy config/settings_example.py to config/settings.py and fill
       in your email/SMS details (see docs/alerts-setup.md).
    2. Wire up the sensors as described in docs/hardware-setup.md.
    3. Calibrate the soil moisture sensor as described in
       docs/hardware-setup.md.

Run with (from the repository root folder):
    python3 plants/tomato_monitor.py
Stop with Ctrl+C
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core import engine

PROFILE = {
    "name": "Tomato",
    "temperature_c": (15, 27),        # combined day (22-27) and night (15-21) band
    "humidity_percent": (60, 70),
    "soil_moisture_percent": (60, 80),  # evenly moist, never waterlogged
    "light_lux": (10000, 130000),       # at least 6-8 hours of strong light daily
    "air_quality_raw_max": 30000,       # general air freshness check, calibrate to your own baseline, see docs/hardware-setup.md
    "notes": (
        "Tomatoes need strong light and warm days with cooler nights. "
        "High humidity combined with wet foliage encourages fungal "
        "disease, so water at the base of the plant, not overhead."
    ),
}

if __name__ == "__main__":
    engine.run_monitor(PROFILE)
