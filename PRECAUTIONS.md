# Precautions

Read this before building and running this system. It covers safety and good practice for both the hardware and the software, separate from the plant-specific precautions in `docs/plant-profiles.md`.

## Electrical and Water Safety

- Never mix mains-voltage wiring (heaters, humidifiers, grow lights, pumps) with the Pi's low-voltage sensor wiring on the same breadboard or enclosure.
- Any mains-powered equipment used near a humid or misted greenhouse environment should be plugged into a properly rated, ideally RCD/GFCI-protected outlet.
- Keep the Raspberry Pi, breadboard, camera, and all exposed wiring away from direct water spray, condensation drips, and splash zones. Use a sealed or weatherproof enclosure for the electronics if your setup involves misting or high humidity, especially for the mushroom profile.
- Turn off power before wiring, rewiring, or moving any sensor.

## Data and Credential Safety

- `config/settings.py` contains your real email password (as an app password) and, if used, your Twilio credentials. Never commit this file to a public GitHub repository. It is already listed in `.gitignore` for exactly this reason; only commit `config/settings_example.py`, which contains placeholder values.
- Use an app password for email, not your actual account password, as described in `docs/alerts-setup.md`.
- If you ever accidentally commit real credentials to a Git repository, treat them as compromised: change the password or regenerate the app password/Twilio token immediately, rather than only removing them from future commits.

## System Reliability

- SD cards can wear out or become corrupted after long-term, frequent writes (constant sensor logging and photo capture add up over months). Consider periodically backing up your `data` folder to another device, and consider a higher-endurance microSD card for long-term deployments.
- Always shut the Pi down properly with `sudo shutdown now` before removing power, to reduce the risk of SD card corruption.
- A brief power interruption will stop the monitor script and it will not restart automatically by default; see the note on `systemd`/`cron @reboot` in `docs/troubleshooting.md` if you want the system to recover automatically after power loss.
- Photos accumulate over time. The built-in retention setting (`PHOTO_RETENTION_DAYS` in `config/settings.py`) automatically deletes old photos, but check your available storage periodically regardless, especially in the early days of running this system.

## Sensor and Alert Limitations

- This system uses low-cost hobby sensors. The MQ135 in particular is not a calibrated CO2 or air-quality-in-ppm sensor, and the soil/substrate moisture percentage is an estimate based on your own two-point calibration, not a scientific measurement. Treat every reading as a helpful trend indicator, not a certified, laboratory-accurate value.
- Alerts are only as good as your thresholds and your sensor placement. A sensor in the wrong spot (for example, in direct sun when the rest of the greenhouse is shaded) will generate misleading readings and alerts.
- This project is intended for hobby, educational, and small personal greenhouse use. It is not a substitute for a certified agricultural monitoring system, and should not be relied on as the sole safeguard for high-value crops, large-scale commercial growing operations, or anything where a missed or delayed alert would cause serious harm or loss.
- This system does not replace regular in-person checks on your plants. Use its alerts as a prompt to go look, not as a full replacement for your own observation.

## General Safety Around Plants and Chemicals

- If you use fertilizers, pesticides, or fungicides in response to something this system alerts you about, follow the product's own safety instructions: wear gloves, ventilate the area, and keep chemicals away from children and pets.
- Mandevilla sap is irritating to skin and toxic if ingested; wear gloves when pruning or handling cuttings, as noted in `docs/plant-profiles.md`.
- Good general hygiene (clean hands and tools) matters for mushroom cultivation specifically, both for successful growing and to avoid mold or contamination issues in an enclosed, humid growing space.

## Privacy

- If your camera has any view beyond your own private growing space (for example, a shared yard, a window facing a public area, or a neighboring property), be mindful of what it captures and where any photos or live feeds might be visible, especially if you ever expose the dashboard beyond your home Wi-Fi network.
- The dashboard in this project is designed to run on your local Wi-Fi network only. Exposing it directly to the public internet is not covered by this project and would need additional security work (authentication, HTTPS, and so on) that is beyond this beginner scope.
