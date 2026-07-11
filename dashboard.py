"""
Wireless greenhouse dashboard.

This is a standalone web app you run alongside one or more plant
monitor scripts. It reads the shared status files those scripts write
to the data folder, and displays live readings, warnings, and the
latest camera photo for each plant currently being monitored.

Run one or more plant monitor scripts first, for example:
    python3 plants/tomato_monitor.py

Then, in a separate terminal, run this dashboard:
    python3 core/dashboard.py

From any device on the same Wi-Fi network, open a browser to:
    http://<your-pi-ip-address>:5000

Find your Pi's IP address by running this on the Pi itself:
    hostname -I
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, render_template_string, send_from_directory

from config import settings

app = Flask(__name__)

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Greenhouse Dashboard</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body { font-family: sans-serif; margin: 30px; background: #f7f7f7; }
        h1 { text-align: center; }
        .card { background: white; border-radius: 10px; padding: 20px; margin: 0 auto 20px auto;
                max-width: 600px; box-shadow: 0 1px 4px rgba(0,0,0,0.15); }
        .card.alert { border-left: 6px solid #b03030; }
        .card.normal { border-left: 6px solid #2f8f2f; }
        .readings { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 10px; }
        .reading { background: #f0f0f0; padding: 8px 12px; border-radius: 6px; font-size: 0.95em; }
        .warnings { color: #b03030; margin-top: 12px; }
        img { max-width: 100%; border-radius: 8px; margin-top: 12px; }
        .timestamp { color: #777; font-size: 0.85em; }
        .empty { text-align: center; color: #555; }
        code { background: #eee; padding: 2px 6px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Greenhouse Dashboard</h1>
    {% if plants %}
        {% for plant in plants %}
        <div class="card {{ 'alert' if plant.status == 'ALERT' else 'normal' }}">
            <h2>{{ plant.plant_name }}</h2>
            <div class="timestamp">Last updated: {{ plant.timestamp }}</div>
            <div class="readings">
                <div class="reading">Temperature: {{ plant.reading.temperature_c }} C</div>
                <div class="reading">Humidity: {{ plant.reading.humidity_percent }} %</div>
                <div class="reading">Light: {{ plant.reading.light_lux }} lux</div>
                <div class="reading">Soil/substrate moisture: {{ plant.reading.soil_moisture_percent }} %</div>
                <div class="reading">Air quality (raw): {{ plant.reading.air_quality_raw }}</div>
            </div>
            {% if plant.warnings %}
            <div class="warnings">
                <strong>Warnings:</strong>
                <ul>
                {% for warning in plant.warnings %}
                    <li>{{ warning }}</li>
                {% endfor %}
                </ul>
            </div>
            {% endif %}
            {% if plant.latest_photo %}
                <img src="/photo/{{ plant.plant_name|lower }}/{{ plant.latest_photo }}" alt="Latest photo of {{ plant.plant_name }}">
            {% endif %}
        </div>
        {% endfor %}
    {% else %}
        <p class="empty">No active monitors found yet. Start a plant monitor script first, for example:<br>
        <code>python3 plants/tomato_monitor.py</code></p>
    {% endif %}
    <p style="text-align:center; color:#888;">This page refreshes automatically every 10 seconds.</p>
</body>
</html>
"""


def _load_all_states():
    data_dir = settings.DATA_DIR
    plants = []
    if not os.path.isdir(data_dir):
        return plants

    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith("_state.json"):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath) as f:
                    plants.append(json.load(f))
            except (OSError, json.JSONDecodeError):
                continue
    return plants


@app.route("/")
def index():
    plants = _load_all_states()
    return render_template_string(PAGE_TEMPLATE, plants=plants)


@app.route("/photo/<plant_slug>/<filename>")
def photo(plant_slug, filename):
    photos_dir = os.path.join(settings.DATA_DIR, "photos", plant_slug)
    return send_from_directory(photos_dir, filename)


@app.route("/api/status")
def api_status():
    return {"plants": _load_all_states()}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
