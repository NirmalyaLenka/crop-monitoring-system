# Smart Greenhouse Monitoring and Automation System

A Raspberry Pi–based IoT greenhouse system designed to monitor and automatically control environmental conditions for different crops. The system collects data from multiple sensors, streams live video from the greenhouse, controls actuators such as irrigation pumps and fans, and provides a web dashboard for remote monitoring and management.

The project is designed to be modular, scalable, and easy to customize for different greenhouse sizes and crop requirements.

---

## Features

### Environmental Monitoring

* Temperature monitoring
* Humidity monitoring
* Soil moisture monitoring
* Ambient light monitoring
* Water tank level monitoring
* Real-time sensor updates

### Automation

* Automatic irrigation
* Automatic fan control
* Automatic humidifier control
* Automatic grow light control
* Manual override mode
* Automatic crop profile switching

### Camera System

* Live video streaming
* Snapshot capture
* Timelapse recording
* Remote greenhouse inspection

### Dashboard

* Live sensor readings
* Device status
* Crop selection
* Camera feed
* Historical graphs
* Manual device controls
* System logs

### Data Management

* SQLite database
* CSV data export
* Historical sensor logs
* Event logging
* Backup support

### Connectivity

* MQTT communication
* REST API
* Local network access
* Remote monitoring support

---

# Supported Crops

The system includes predefined environmental profiles for multiple crops.

| Crop            | Temperature | Humidity | Soil Moisture |
| --------------- | ----------- | -------- | ------------- |
| Tomato          | 21–27°C     | 60–70%   | 60–80%        |
| Capsicum        | 20–26°C     | 65–80%   | 60–75%        |
| Spinach         | 15–24°C     | 50–70%   | 70–80%        |
| Grapes          | 22–30°C     | 50–70%   | 40–60%        |
| Oyster Mushroom | 15–21°C     | 85–95%   | 80–90%        |

Crop profiles can be modified or new crops can be added through the configuration file without changing the source code.

---

# Hardware Used

## Main Controller

* Raspberry Pi 4

## Sensors

* SHT31 Temperature & Humidity Sensor
* BH1750 Light Sensor
* Capacitive Soil Moisture Sensor
* Float Switch (Water Tank Level)

## Actuators

* 4-Channel Relay Module
* 12V Brushless Cooling Fan
* 12V Water Pump
* Ultrasonic Humidifier
* Full Spectrum LED Grow Light

## Camera

* Raspberry Pi Camera Module 3

---

# Software Stack

* Python 3
* Flask
* SQLite
* MQTT
* OpenCV
* Picamera2
* Bootstrap 5
* HTML
* CSS
* JavaScript
* Chart.js

---

# Project Structure

```text
Smart-Greenhouse-System/
│
├── app.py
├── requirements.txt
├── install.sh
├── greenhouse.service
├── README.md
│
├── config/
├── database/
├── docs/
├── logs/
├── scripts/
│
├── src/
│   ├── actuators/
│   ├── api/
│   ├── camera/
│   ├── control/
│   ├── mqtt/
│   ├── sensors/
│   └── utils/
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/
└── tests/
```

---

# System Architecture

```text
                     Raspberry Pi

        +---------------------------------------+
        |          Flask Web Dashboard          |
        +---------------------------------------+
                      |
        +---------------------------------------+
        |      Climate Control Application      |
        +---------------------------------------+
          |         |         |         |
          |         |         |         |
       Sensors   Camera    MQTT     Database
          |
   -----------------------------
   |     |      |       |
 SHT31  BH1750 Soil   Float
                 Sensor Switch
          |
      Decision Engine
          |
      Relay Controller
          |
 -------------------------------
 |      |      |       |
 Fan   Pump Humidifier Lights
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/Smart-Greenhouse-System.git
```

Open the project directory.

```bash
cd Smart-Greenhouse-System
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
python app.py
```

---

# Crop Automation Logic

The automation engine continuously compares live sensor values with the selected crop profile.

If:

* Temperature exceeds the maximum limit, the cooling fan is activated.
* Humidity drops below the minimum value, the humidifier starts.
* Soil moisture becomes too low, irrigation begins.
* Light intensity falls below the configured threshold, the grow lights turn on.

Each device automatically switches off when the desired conditions are restored.

---

# Future Improvements

* AI-based plant disease detection
* Machine learning for crop prediction
* Weather forecast integration
* Mobile application
* Voice assistant support
* ESP32 wireless sensor nodes
* Solar power monitoring
* Power consumption analytics
* Multi-greenhouse support
* Cloud synchronization

---

# Contributing

Contributions are welcome. If you would like to improve the project, feel free to fork the repository, create a new branch, and submit a pull request.

---

# License

This project is licensed under the MIT License.

---

# Author

**Nirmalya Lenka**

Electrical and Computer Engineering Student

This project was developed as a practical IoT solution for greenhouse automation using Raspberry Pi, environmental sensors, and intelligent climate control.
## this is just a trial version please visite the main file to see the project files.
