"""
Email and SMS alert functions for the greenhouse monitoring system.

Email uses a standard SMTP connection. This works well with a Gmail
app password; see docs/alerts-setup.md for how to create one.

SMS uses Twilio, which requires a free trial or paid Twilio account.
SMS is optional: if SMS_ALERTS["enabled"] is False in config/settings.py,
this module skips texting entirely and only sends email.

Both alert types share a cooldown system, so a single ongoing problem
(for example, a heater stuck on) sends one alert and then waits before
repeating it, instead of flooding your inbox and phone every minute.
"""

from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib

from config import settings

_last_alert_times = {}


def _cooldown_has_passed(alert_key):
    now = datetime.now()
    last_time = _last_alert_times.get(alert_key)
    if last_time is None:
        return True
    return now - last_time > timedelta(minutes=settings.ALERT_COOLDOWN_MINUTES)


def _mark_alert_sent(alert_key):
    _last_alert_times[alert_key] = datetime.now()


def send_email_alert(subject, body, image_path=None):
    if not settings.EMAIL_ALERTS.get("enabled"):
        return False

    try:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = settings.EMAIL_ALERTS["sender_email"]
        message["To"] = settings.EMAIL_ALERTS["recipient_email"]
        message.set_content(body)

        if image_path:
            with open(image_path, "rb") as f:
                image_data = f.read()
            message.add_attachment(
                image_data, maintype="image", subtype="jpeg", filename="greenhouse.jpg"
            )

        with smtplib.SMTP(
            settings.EMAIL_ALERTS["smtp_server"], settings.EMAIL_ALERTS["smtp_port"]
        ) as server:
            server.starttls()
            server.login(
                settings.EMAIL_ALERTS["sender_email"],
                settings.EMAIL_ALERTS["sender_app_password"],
            )
            server.send_message(message)

        return True
    except Exception as error:
        print("Email alert failed:", error)
        return False


def send_sms_alert(message_text):
    if not settings.SMS_ALERTS.get("enabled"):
        return False

    try:
        from twilio.rest import Client

        client = Client(
            settings.SMS_ALERTS["twilio_account_sid"],
            settings.SMS_ALERTS["twilio_auth_token"],
        )
        client.messages.create(
            body=message_text,
            from_=settings.SMS_ALERTS["twilio_from_number"],
            to=settings.SMS_ALERTS["owner_phone_number"],
        )
        return True
    except Exception as error:
        print("SMS alert failed:", error)
        return False


def send_alert_if_needed(alert_key, subject, body, image_path=None):
    """
    Sends both an email and an SMS alert (SMS only if enabled) for
    alert_key, unless an alert with the same key was already sent
    within the cooldown period set in settings.ALERT_COOLDOWN_MINUTES.
    Returns True if an alert was actually sent.
    """
    if not _cooldown_has_passed(alert_key):
        return False

    send_email_alert(subject, body, image_path)
    send_sms_alert(body)
    _mark_alert_sent(alert_key)
    return True
