# Hardware Setup

Full parts list, wiring, and calibration steps for the greenhouse monitoring system. Read this fully before wiring anything.

## Parts List

| Part | Purpose |
|---|---|
| Raspberry Pi (3, 4, or 5) with Raspberry Pi OS installed | Runs all the monitoring code |
| DHT22 sensor | Temperature and humidity |
| BH1750 light sensor (I2C) | Light level in lux |
| Capacitive soil/substrate moisture sensor | Moisture reading |
| MQ135 air quality sensor | General air quality / gas presence |
| MCP3008 analog-to-digital converter chip | Lets the Pi read the analog moisture and MQ135 sensors, since the Pi has no analog input pins |
| Raspberry Pi Camera Module | Visual monitoring and photo logging |
| Breadboard and jumper wires | Wiring everything together |
| 5V power supply for the Pi | Official supply recommended |

## Wiring

### DHT22 (temperature and humidity)

```
VCC -> 5V (or 3.3V, check your specific module)
GND -> GND
DATA -> GPIO4
```

A 10k pull-up resistor between DATA and VCC is recommended if your module does not already include one on its small breakout board.

### BH1750 (light sensor, I2C)

```
VCC -> 3.3V
GND -> GND
SCL -> GPIO3 (SCL)
SDA -> GPIO2 (SDA)
```

Enable I2C first:

```
sudo raspi-config
```

Interface Options -> I2C -> Enable, then reboot.

Confirm the sensor is detected:

```
sudo apt install -y i2c-tools
i2cdetect -y 1
```

You should see `23` appear in the grid, which is the BH1750's default I2C address.

### MCP3008 (needed for the analog sensors)

```
VDD  -> 3.3V
VREF -> 3.3V
AGND -> GND
DGND -> GND
CLK  -> GPIO11 (SPI SCLK)
DOUT -> GPIO9  (SPI MISO)
DIN  -> GPIO10 (SPI MOSI)
CS   -> GPIO8  (SPI CE0)
```

Enable SPI first:

```
sudo raspi-config
```

Interface Options -> SPI -> Enable, then reboot.

### Soil/Substrate Moisture Sensor

```
VCC -> 3.3V
GND -> GND
AOUT -> MCP3008 channel 0
```

### MQ135 Air Quality Sensor

```
VCC -> 5V
GND -> GND
AOUT -> MCP3008 channel 1
```

MQ135 modules need a warm-up period of several minutes after power-on before readings settle. Do not trust readings taken in the first few minutes after powering on.

### Camera

Connect the camera ribbon cable to the CSI camera port. The connector differs between Pi 3/Pi 4 and Pi 5, so use the correct cable for your board. See the separate raspberry-pi-camera-guide project in this collection for full camera wiring, testing, and troubleshooting steps.

## Calibrating the Soil/Substrate Moisture Sensor

The raw values from a capacitive moisture sensor vary between individual units, so you need to calibrate your specific sensor:

1. With the sensor completely dry, in open air, run a short Python script that prints `sensors.read_soil_moisture_percent()`'s underlying raw channel value (or add a temporary print statement), and note the raw value. This is your `dry_raw`.
2. Submerge only the sensing portion of the probe in a cup of water and note the raw value again. This is your `wet_raw`.
3. Open `core/sensors.py` and update the default `dry_raw` and `wet_raw` values in `read_soil_moisture_percent()` to match your own readings.
4. Never submerge the sensor's exposed circuit board, only the marked sensing area, or you risk damaging it.

## Calibrating the Air Quality (MQ135) Baseline

The MQ135 does not give a calibrated ppm or CO2 value out of the box. To make its readings useful:

1. Let the sensor warm up for at least 20 to 30 minutes in the actual environment you plan to monitor, with normal fresh air circulation.
2. Note the typical raw value it settles around. This is your fresh-air baseline.
3. Set each plant's `air_quality_raw_max` in its script under the `plants` folder to a value somewhat above that baseline, so the alert only fires when air quality noticeably worsens compared to your own normal conditions, rather than relying on an absolute number that means something different for every individual sensor unit.
4. Re-check this baseline occasionally, since MQ135 sensors can drift over weeks and months of continuous use.

## General Wiring Safety

- Always power off the Pi before wiring or rewiring anything.
- Never connect a GPIO pin directly to 5V. GPIO pins operate at 3.3V logic level.
- Double check polarity before connecting any sensor.
- Keep all electronics, wiring, and the Pi itself away from direct water spray, misting nozzles, and splash zones. Use a sealed enclosure or waterproof project box for the Pi and breadboard if humidity or misting is part of your greenhouse setup, especially for the mushroom profile which requires very high humidity.
- If your greenhouse setup includes mains-powered equipment (heaters, humidifiers, pumps), keep that wiring completely separate from the low-voltage Pi wiring, and use a properly rated, ideally RCD/GFCI-protected outlet for anything combining electricity and moisture.
