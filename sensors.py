"""
Sensor reading functions for the greenhouse monitoring system.

Hardware used by every plant profile in this repository:

    DHT22 (temperature + humidity)      -> GPIO4
    BH1750 light sensor (I2C, digital)  -> SDA (GPIO2), SCL (GPIO3)
    Capacitive soil/substrate moisture  -> MCP3008 channel 0
    MQ135 air quality sensor            -> MCP3008 channel 1

    MCP3008 (needed because the Pi has no analog input pins):
        VDD  -> 3.3V
        VREF -> 3.3V
        AGND -> GND
        DGND -> GND
        CLK  -> GPIO11 (SPI SCLK)
        DOUT -> GPIO9  (SPI MISO)
        DIN  -> GPIO10 (SPI MOSI)
        CS   -> GPIO8  (SPI CE0)

Full wiring diagrams, photos-in-words, and calibration steps are in
docs/hardware-setup.md. Read that file before wiring anything.

Enable both I2C and SPI first with:
    sudo raspi-config
    (Interface Options -> I2C -> Enable)
    (Interface Options -> SPI -> Enable)

Install requirements first:
    pip3 install -r requirements.txt --break-system-packages
    sudo apt install -y libgpiod2

Every read function below returns None for a value it could not read,
instead of crashing, so a single loose wire or a bad DHT22 read does
not bring down the whole monitoring loop.
"""

import time

import board
import busio
import digitalio
import adafruit_dht
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import smbus2

# ---- DHT22 setup ----
_dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# ---- MCP3008 setup (shared SPI bus for soil/substrate moisture and MQ135) ----
_spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
_cs = digitalio.DigitalInOut(board.CE0)
_mcp = MCP.MCP3008(_spi, _cs)
_soil_channel = AnalogIn(_mcp, MCP.P0)
_gas_channel = AnalogIn(_mcp, MCP.P1)

# ---- BH1750 light sensor setup (I2C) ----
_BH1750_ADDRESS = 0x23
_BH1750_CONTINUOUS_HIGH_RES_MODE = 0x10
_i2c_bus = smbus2.SMBus(1)


def read_temperature_humidity():
    """Returns (temperature_celsius, humidity_percent). Either can be None on a failed read."""
    try:
        temperature_c = _dht_device.temperature
        humidity_percent = _dht_device.humidity
        return temperature_c, humidity_percent
    except RuntimeError:
        # DHT sensors fail an individual read fairly often, this is
        # normal and the next cycle will usually succeed.
        return None, None


def read_light_lux():
    """Returns light level in lux from the BH1750 sensor, or None on failure."""
    try:
        _i2c_bus.write_byte(_BH1750_ADDRESS, _BH1750_CONTINUOUS_HIGH_RES_MODE)
        time.sleep(0.2)
        data = _i2c_bus.read_i2c_block_data(_BH1750_ADDRESS, _BH1750_CONTINUOUS_HIGH_RES_MODE, 2)
        raw = (data[0] << 8) + data[1]
        lux = raw / 1.2
        return round(lux, 1)
    except OSError:
        return None


def read_soil_moisture_percent(dry_raw=26000, wet_raw=9000):
    """
    Returns an estimated moisture percentage from the capacitive
    soil/substrate probe, based on two calibration points.

    dry_raw and wet_raw are the raw MCP3008 readings you get with the
    probe fully dry in open air, and fully submerged in water. These
    values vary between individual sensor units, so calibrate your own
    probe using the steps in docs/hardware-setup.md and update these
    two numbers to match.
    """
    try:
        raw = _soil_channel.value
        raw = max(min(raw, dry_raw), wet_raw)
        percent = (dry_raw - raw) / (dry_raw - wet_raw) * 100
        return round(percent, 1)
    except OSError:
        return None


def read_air_quality_raw():
    """
    Returns (raw_value, voltage) from the MQ135 sensor.

    This is NOT a calibrated ppm/CO2 reading. The MQ135 is a low-cost
    hobby sensor, and its raw output only tells you a relative gas
    concentration compared to your own baseline reading in fresh air.
    Calibrate your own baseline and thresholds as described in
    docs/hardware-setup.md.
    """
    try:
        return _gas_channel.value, round(_gas_channel.voltage, 3)
    except OSError:
        return None, None


def read_all():
    """Reads every sensor once and returns a single dictionary of results."""
    temperature_c, humidity_percent = read_temperature_humidity()
    light_lux = read_light_lux()
    soil_moisture_percent = read_soil_moisture_percent()
    air_quality_raw, air_quality_voltage = read_air_quality_raw()

    return {
        "temperature_c": temperature_c,
        "humidity_percent": humidity_percent,
        "light_lux": light_lux,
        "soil_moisture_percent": soil_moisture_percent,
        "air_quality_raw": air_quality_raw,
        "air_quality_voltage": air_quality_voltage,
    }
