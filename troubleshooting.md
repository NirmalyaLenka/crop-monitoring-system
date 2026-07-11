# Troubleshooting

## "RuntimeError" or Missing Readings from the DHT22

DHT22 sensors fail an individual read fairly often, this is normal and expected. `core/sensors.py` already handles this by returning `None` and letting the next cycle try again. If it fails on every single cycle for several minutes in a row:

- Check the wiring, especially the data pin and any pull-up resistor.
- Try a different GPIO pin and update `board.D4` in `core/sensors.py` to match.
- Confirm the sensor is not damaged; DHT22 modules can fail permanently if powered incorrectly.

## BH1750 Light Sensor Not Detected

- Confirm I2C is enabled: `sudo raspi-config` -> Interface Options -> I2C.
- Run `i2cdetect -y 1` and confirm `23` appears in the results.
- Check wiring: SDA to GPIO2, SCL to GPIO3, and confirm the sensor is powered at 3.3V.

## MCP3008 Readings Look Wrong or Stuck

- Confirm SPI is enabled: `sudo raspi-config` -> Interface Options -> SPI.
- Double check all seven MCP3008 wiring connections listed in `docs/hardware-setup.md`, especially VREF, since a missing VREF connection causes flat, incorrect readings.
- Confirm you are reading the correct channel (`MCP.P0` for soil/substrate moisture, `MCP.P1` for the MQ135).

## Soil/Substrate Moisture Percentage Seems Backwards or Never Changes

- Recalibrate `dry_raw` and `wet_raw` in `core/sensors.py` using the steps in `docs/hardware-setup.md`. These defaults are only a starting point and vary by individual sensor unit.
- Confirm the sensor's exposed probe area, not its circuit board, is what is inserted into soil or substrate.

## MQ135 Air Quality Alerts Fire Constantly or Never

- The MQ135 needs a genuine warm-up period (20 to 30 minutes) before its readings are meaningful.
- Recalibrate `air_quality_raw_max` in the relevant plant script to a value clearly above your own fresh-air baseline, as described in `docs/hardware-setup.md`. The default placeholder values are only a starting point.

## Email Alerts Not Arriving

- Confirm you are using a Gmail app password, not your regular account password. See `docs/alerts-setup.md`.
- Check your spam or junk folder.
- Confirm `EMAIL_ALERTS["enabled"]` is `True` in `config/settings.py`.
- Look at the terminal output where the monitor script is running; failed email attempts print an error message describing what went wrong.

## SMS Alerts Not Arriving

- Confirm `SMS_ALERTS["enabled"]` is `True` in `config/settings.py`.
- On a Twilio trial account, confirm the destination number has been manually verified in the Twilio console; trial accounts cannot text unverified numbers.
- Confirm your Twilio account still has trial credit or a valid payment method attached.

## Camera Errors ("Failed to acquire camera")

- Make sure no other program or leftover process is already using the camera. Reboot the Pi to release any stuck camera resources.
- Confirm the camera is properly connected; see the separate raspberry-pi-camera-guide project for full camera-specific troubleshooting.

## Dashboard Shows "No active monitors found yet"

- The dashboard only displays a plant once its monitor script has completed at least one full reading cycle and written its first status file.
- Confirm the plant monitor script is actually running in another terminal or session, and check its terminal output for errors.
- Confirm both the monitor script and the dashboard are pointed at the same `DATA_DIR` in `config/settings.py`.

## Cannot Reach the Dashboard from Another Device

- Confirm your other device is on the same Wi-Fi network as the Pi.
- Run `hostname -I` on the Pi to get its correct current IP address, and use `http://<that-ip>:5000` exactly.
- Confirm no firewall on your router or Pi is blocking port 5000.

## The Pi Restarted and Monitoring Stopped

By default, the monitor scripts do not restart automatically after a reboot or power interruption. For unattended long-term use, consider setting up a `systemd` service or a `cron @reboot` entry to automatically start your chosen plant monitor script (and the dashboard) whenever the Pi boots up. This is an intermediate Linux topic; search "run python script on raspberry pi boot systemd" for a full walkthrough once you are comfortable with the basics in this repository.
