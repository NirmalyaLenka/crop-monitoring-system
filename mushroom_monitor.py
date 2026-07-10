"""
Greenhouse monitor for oyster mushroom cultivation (fruiting stage).

The ranges below reflect typical oyster mushroom fruiting chamber
guidance: cool stable temperatures, very high humidity, low indirect
light, and low CO2 buildup through frequent fresh air exchange. See
docs/plant-profiles.md for full research notes, sources, and
precautions specific to mushrooms.

Before running this script:
    1. Copy config/settings_example.py to config/settings.py and fill
       in your email/SMS details (see docs/alerts-setup.md).
    2. Wire up the sensors as described in docs/hardware-setup.md.
    3. Calibrate the substrate moisture sensor and the air quality
       baseline as described in docs/hardware-setup.md. Mushroom
       substrate behaves very differently from garden soil, and the
       MQ135 needs a fresh-air baseline reading to be useful at all.

Run with (from the repository root folder):
    python3 plants/mushroom_monitor.py
Stop with Ctrl+C
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core import engine

PROFILE = {
    "name": "Mushroom",
    "temperature_c": (15, 21),
    "humidity_percent": (85, 95),
    "soil_moisture_percent": (70, 95),  # substrate moisture, calibrate carefully, see docs/hardware-setup.md
    "light_lux": (200, 1000),           # low, indirect/diffused light only, 10-12 hours per day
    "air_quality_raw_max": 20000,       # mushrooms are especially sensitive to CO2 buildup; calibrate to your own fresh-air baseline
    "notes": (
        "Oyster mushrooms need high humidity, cool stable temperatures, "
        "low indirect light, and frequent fresh air exchange to prevent "
        "CO2 buildup, which can cause long thin stems and small, "
        "underdeveloped caps if ignored."
    ),
}

if __name__ == "__main__":
    engine.run_monitor(PROFILE)
