# Greenhouse Monitoring System

A beginner-friendly, Raspberry Pi based greenhouse monitoring system with sensors, a camera, data storage, a live wireless dashboard, and email/SMS alerts. It ships with ready-to-run monitoring profiles for five different plants: mushroom, tomato, citrus, pepper, and Mandevilla.

No prior experience with Linux, electronics, or Python is required, though this is a bigger project than a single sensor script, so budget more time than a simple blink or single-sensor project.

Read `PRECAUTIONS.md` before building or running this system. It covers electrical safety, credential safety, and the real limitations of hobby sensors.

## What This System Does

1. Reads temperature, humidity, light level, soil/substrate moisture, and air quality from a set of sensors, on a repeating schedule.
2. Logs every reading to a CSV file you can open in any spreadsheet program.
3. Takes a timestamped camera photo on a repeating schedule, and automatically deletes old photos after a configurable number of days.
4. Compares every reading against ideal ranges for whichever plant you are monitoring, and sends you an email (and optionally an SMS text) if something is out of range, with a cooldown so you are not flooded with repeat alerts.
5. Runs a small live dashboard web page, viewable from your phone or laptop over your home Wi-Fi, showing the current status and latest photo for every plant you are monitoring.

## How the Project Is Organized

```
greenhouse-monitoring-system/
├── config/
│   └── settings_example.py   Copy to settings.py and fill in your own values
├── core/
│   ├── sensors.py            Reads the DHT22, BH1750, soil/substrate probe, and MQ135
│   ├── camera_capture.py     Takes and stores timestamped photos
│   ├── alerts.py             Sends email and optional SMS alerts, with cooldown
│   ├── data_logger.py        Appends sensor readings to a CSV file
│   ├── engine.py             The shared monitoring loop every plant script uses
│   └── dashboard.py          The live web dashboard, run separately
├── plants/
│   ├── mushroom_monitor.py
│   ├── tomato_monitor.py
│   ├── citrus_monitor.py
│   ├── pepper_monitor.py
│   └── mandevilla_monitor.py
└── docs/
    ├── hardware-setup.md     Full wiring and calibration instructions
    ├── plant-profiles.md     Research notes, values, and precautions per plant
    ├── alerts-setup.md       Gmail app password and Twilio SMS setup
    └── troubleshooting.md    Fixes for common problems
```

Every plant script in `plants/` is short on purpose: it only defines that plant's ideal ranges and a couple of notes, then hands off to the shared logic in `core/engine.py`. This means all five plant scripts behave identically in terms of logging, photos, alerts, and the dashboard; only the thresholds differ.

## Quick Start

1. Set up your Pi, wire the sensors and camera, and enable I2C and SPI following `docs/hardware-setup.md` in full.
2. Install the required software:

```
sudo apt update
sudo apt install -y python3-picamera2 i2c-tools libgpiod2
pip3 install -r requirements.txt --break-system-packages
```

3. Copy the settings template and fill in your details:

```
cp config/settings_example.py config/settings.py
```

Follow `docs/alerts-setup.md` to fill in your email (and optional SMS) details in `config/settings.py`.

4. Calibrate your soil/substrate moisture sensor and your air quality baseline, following the steps in `docs/hardware-setup.md`.
5. Run the monitor script for whichever plant you are growing, from the repository's root folder:

```
python3 plants/tomato_monitor.py
```

6. In a separate terminal, run the live dashboard:

```
python3 core/dashboard.py
```

7. From your phone or laptop, on the same Wi-Fi network, open a browser to `http://<your-pi-ip-address>:5000`. Find your Pi's IP address by running `hostname -I` on the Pi itself.

## Ideal Ranges at a Glance

These are simplified single day/night bands for quick reference. Full reasoning, sources, and precautions for each plant are in `docs/plant-profiles.md`, which you should read before relying on any of these values.

| Plant | Temperature | Humidity | Soil/substrate moisture | Light |
|---|---|---|---|---|
| Mushroom | 15 to 21 C | 85 to 95% | 70 to 95% | 200 to 1000 lux |
| Tomato | 15 to 27 C | 60 to 70% | 60 to 80% | 10,000 to 130,000 lux |
| Citrus | 10 to 29 C | 50 to 60% | 35 to 65% | 8,000 to 130,000 lux |
| Pepper | 15 to 27 C | 50 to 70% | 55 to 75% | 10,000 to 130,000 lux |
| Mandevilla | 15 to 32 C | 50 to 60% | 45 to 70% | 8,000 to 130,000 lux |

Air quality is not included in this table since the MQ135 needs to be calibrated to your own environment's fresh-air baseline rather than compared against a fixed universal number; see `docs/hardware-setup.md`.

## Monitoring More Than One Plant at Once

You can run more than one plant monitor script at the same time (for example, in separate terminal sessions, or using `screen`/`tmux`), as long as each one is monitoring a genuinely separate set of sensors and its own camera setup. The shared dashboard will automatically show every plant currently being monitored, since each plant script writes its own separate status file.

Running two scripts that try to use the exact same physical sensor or camera at the same time will cause conflicts; this project assumes one full sensor and camera set per plant being actively monitored.

## Precautions

See `PRECAUTIONS.md` for the full list, but in short:

- Keep electronics away from water spray and high humidity, use a sealed enclosure where needed.
- Never commit `config/settings.py` (it holds your real credentials); only `config/settings_example.py` should be committed.
- Treat every sensor reading as a helpful estimate from a low-cost hobby sensor, not a certified, laboratory-accurate measurement.
- This system is for hobby, educational, and small personal greenhouse use, not a substitute for a certified agricultural monitoring system or for your own regular in-person checks on your plants.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Please visit the link for ease to find the file and implementation. 
 link: https://nirmalyalenka.github.io/crop-monitoring-system/
