"""
Configuration template for the greenhouse monitoring system.

Copy this file to settings.py in this same config folder, then fill in
your own values:

    cp config/settings_example.py config/settings.py

settings.py is listed in .gitignore, so your real email password and
any SMS credentials are never accidentally committed to GitHub. Only
settings_example.py (with placeholder values) should ever be pushed.
"""

# Folder where logs, photos, and status files are stored
DATA_DIR = "data"

# How often to take a sensor reading, in seconds
READING_INTERVAL_SECONDS = 60

# How often to capture a camera photo, in minutes
PHOTO_INTERVAL_MINUTES = 30

# How many days of photos to keep before old ones are deleted automatically
PHOTO_RETENTION_DAYS = 14

# Minimum time between repeated alerts for the same plant, in minutes,
# so a single ongoing problem does not flood your inbox or phone
ALERT_COOLDOWN_MINUTES = 30

# Email alerts, sent through a normal SMTP connection.
# See docs/alerts-setup.md for how to create a Gmail app password.
EMAIL_ALERTS = {
    "enabled": True,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-address@gmail.com",
    "sender_app_password": "your-16-character-app-password",
    "recipient_email": "owner-address@example.com",
}

# SMS alerts are optional and use Twilio. Leave "enabled" as False if
# you only want email alerts. See docs/alerts-setup.md for how to get
# these values from a Twilio account.
SMS_ALERTS = {
    "enabled": False,
    "twilio_account_sid": "",
    "twilio_auth_token": "",
    "twilio_from_number": "",
    "owner_phone_number": "",
}
