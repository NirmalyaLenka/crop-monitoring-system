# Raspberry Pi Greenhouse Monitoring System

A modular Raspberry Pi monitoring prototype for greenhouse and indoor growing experiments. It reads environmental sensors, logs measurements, captures periodic photos, compares readings with plant-specific ranges, and can send email/SMS alerts. A local Flask dashboard displays the latest status over the LAN.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Raspberry Pi](https://img.shields.io/badge/Platform-Raspberry%20Pi-C51A4A?logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/)
[![Flask](https://img.shields.io/badge/Dashboard-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Prototype-orange)](./)

## What it does

- Reads temperature and humidity using a DHT22, light level via I²C, and analogue moisture/air-quality signals through an MCP3008 ADC.
- Writes timestamped readings to CSV files and stores camera images.
- Compares readings against configurable plant profiles for mushroom, tomato, citrus, pepper, and Mandevilla.
- Sends email alerts and optional SMS alerts when readings leave the configured ranges, with a cooldown to limit repeated notifications.
- Serves a local dashboard that displays recent readings, warnings, and photos.

This is a **monitoring and alerting prototype**, not an automatic climate-control system. Hobby sensors require calibration and can produce misleading values. Do not use it as the sole safety or crop-management system.

## How it works

1. A plant profile in `plants/` defines the target ranges and calls the shared monitoring engine.
2. `core/sensors.py` reads the connected sensors; unavailable readings are represented as missing values rather than treated as valid measurements.
3. `core/engine.py` checks ranges, writes CSV data, manages periodic photo capture, and triggers alerts.
4. `core/dashboard.py` reads the shared status files and serves a local web dashboard.
5. `config/settings.py` contains local runtime settings and notification credentials. Create it from the example file; never commit real credentials.

## Hardware

The current sensor implementation and comments describe this typical setup:

| Component | Purpose | Notes |
|---|---|---|
| Raspberry Pi 3/4/5 | Main controller | Enable I²C and SPI using `sudo raspi-config`. |
| DHT22 | Air temperature and relative humidity | Confirm the GPIO pin and pull-up arrangement in `core/sensors.py`. |
| BH1750 / I²C light sensor | Light-level measurement | Confirm address and wiring in `docs/hardware-setup.md`. |
| MCP3008 ADC | Converts analogue sensor outputs | Used because Raspberry Pi GPIO has no built-in analogue input. |
| Capacitive moisture probe | Soil/substrate moisture estimate | Calibrate for the actual soil or growing substrate. |
| MQ135 module | Rough air-quality trend | Not a calibrated safety gas detector. |
| Pi camera + Picamera2 | Periodic photos | Install the system package appropriate for the Raspberry Pi OS version. |

Read [hardware setup](docs/hardware-setup.md) and [precautions](PRECAUTIONS.md) before connecting hardware. Check each sensor's supply voltage and pinout; do not assume every breakout is 3.3 V tolerant.

## Setup

These instructions target Raspberry Pi OS. Camera support and GPIO libraries depend on the OS release and board.

### 1. Install system packages

```bash
sudo apt update
sudo apt install -y python3-venv python3-picamera2 libgpiod2
```

Enable I²C and SPI with `sudo raspi-config`, then reboot if requested.

### 2. Create a virtual environment

The `--system-site-packages` option allows the virtual environment to use the system-installed Picamera2 package.

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Add local settings

```bash
cp config/settings_example.py config/settings.py
```

Edit `config/settings.py` for your local data paths and notification settings. Keep real email app passwords and Twilio credentials out of Git.

### 4. Start one plant monitor

Run commands from the repository root. For example:

```bash
python plants/tomato_monitor.py
```

Other profiles are in `plants/`. Check each profile's comments and the research notes before using its ranges for real cultivation.

### 5. Start the dashboard

In a second terminal, activate the same virtual environment and run:

```bash
source .venv/bin/activate
python core/dashboard.py
```

Open `http://<raspberry-pi-ip>:5000` from a device on the same network. Find the Pi address with `hostname -I`.

## Repository structure

```text
.
├── config/
│   ├── __init__.py
│   └── settings_example.py       # Safe template; copy to ignored settings.py
├── core/
│   ├── __init__.py
│   ├── alerts.py                 # Email and optional SMS notifications
│   ├── camera_capture.py         # Picamera2 capture and photo retention
│   ├── dashboard.py              # Flask LAN dashboard
│   ├── data_logger.py            # CSV logging
│   ├── engine.py                 # Shared monitoring loop and thresholds
│   └── sensors.py                # DHT22, ADC and sensor access
├── plants/
│   ├── __init__.py
│   ├── citrus_monitor.py
│   ├── mandevilla_monitor.py
│   ├── mushroom_monitor.py
│   ├── pepper_monitor.py
│   └── tomato_monitor.py
├── docs/
│   ├── alerts-setup.md
│   ├── hardware-setup.md
│   ├── plant-profiles.md
│   ├── project_log_mockup.html   # Static reference page; not the live Flask dashboard
│   └── troubleshooting.md
├── data/                         # Generated readings/status; ignored by Git
├── photos/                       # Generated images; ignored by Git
├── PRECAUTIONS.md
├── requirements.txt
└── README.md
```

## Documentation

- [Hardware wiring and setup](docs/hardware-setup.md)
- [Plant profile notes and sources](docs/plant-profiles.md)
- [Email/SMS setup](docs/alerts-setup.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Safety and limitations](PRECAUTIONS.md)

## Skills demonstrated

- Raspberry Pi and Linux setup
- Python modules and package structure
- Sensor integration, I²C, SPI and ADC interfaces
- Flask dashboards and LAN access
- CSV logging, threshold checks, and notification workflows
- Hardware calibration and troubleshooting

## Known limitations

- The project has not been hardware-validated as part of this documentation/layout cleanup.
- Sensor readings need calibration; plant target ranges are simplified guidance, not a guarantee of healthy growth.
- Email and SMS require correct local credentials and network access.
- Picamera2/GPIO setup varies by Raspberry Pi OS version.
- The dashboard is intended for a trusted local network. Do not expose it directly to the public internet.

## Maintenance & validation

- **Documentation/layout review:** 11 November 2026.
- **Changes:** Files were placed into the `core/`, `plants/`, `config/`, and `docs/` packages that the code and setup instructions already expected.
- **Validation status:** Imports and hardware execution have not been run on a Raspberry Pi in this session. Follow the setup steps and verify each sensor before relying on the system.
