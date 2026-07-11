# Setting Up Email and SMS Alerts

This system can notify you by email, and optionally by SMS text message, whenever a plant's readings go out of range.

## Email Alerts (Gmail)

Gmail no longer allows sign-in with just your regular password from scripts like this one. You need to create an "app password" instead.

1. Go to your Google Account settings and turn on 2-Step Verification if it is not already on. An app password cannot be created without it.
2. Search your Google Account settings for "App passwords".
3. Create a new app password. Give it a name like "Greenhouse Monitor".
4. Google will show you a 16-character password. Copy it.
5. Open `config/settings.py` (copy it from `config/settings_example.py` first if you have not already) and fill in:

```python
EMAIL_ALERTS = {
    "enabled": True,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-address@gmail.com",
    "sender_app_password": "the 16-character app password",
    "recipient_email": "owner-address@example.com",
}
```

`sender_email` is the Gmail account sending the alert. `recipient_email` is where you want alerts delivered, which can be the same address or a different one (including a phone carrier's email-to-SMS gateway address, if your carrier offers one, as a free alternative to Twilio).

6. Never commit `config/settings.py` to a public GitHub repository. It is already listed in `.gitignore` for this reason.

If you use a different email provider instead of Gmail, replace `smtp_server` and `smtp_port` with your provider's SMTP details, and check whether it also requires an app password rather than your normal login password.

## SMS Alerts (Twilio, Optional)

SMS is optional. If you only want email alerts, leave `SMS_ALERTS["enabled"]` as `False` in `config/settings.py` and skip this section.

1. Create a free account at Twilio's website.
2. A trial account gives you a small amount of free credit and a temporary phone number.
3. From the Twilio console dashboard, copy your **Account SID** and **Auth Token**.
4. Note the Twilio phone number assigned to your trial account, in the format `+1XXXXXXXXXX`.
5. Trial accounts can only send SMS to phone numbers you have manually verified in the Twilio console. Add and verify the phone number you want alerts sent to.
6. Open `config/settings.py` and fill in:

```python
SMS_ALERTS = {
    "enabled": True,
    "twilio_account_sid": "your account SID",
    "twilio_auth_token": "your auth token",
    "twilio_from_number": "+1XXXXXXXXXX",
    "owner_phone_number": "+91XXXXXXXXXX",
}
```

7. Install the Twilio Python library if you have not already, it is included in `requirements.txt`:

```
pip3 install -r requirements.txt --break-system-packages
```

Twilio SMS costs real money once trial credit runs out, so keep this in mind for a long-running unattended setup, and check Twilio's current pricing before relying on it for regular alerts.

## Alert Cooldown

Both email and SMS alerts share a single cooldown timer per plant, set by `ALERT_COOLDOWN_MINUTES` in `config/settings.py`. This stops a single ongoing issue (for example, a stuck heater keeping the temperature too high) from sending a new alert every single monitoring cycle. Increase this value if you are getting alerted more often than you would like, or decrease it if you want faster repeat notifications for genuinely urgent conditions.

## Testing Alerts

Before relying on this system, deliberately trigger a test alert to confirm delivery works, for example by temporarily setting an unrealistic threshold (like `"temperature_c": (100, 200)`) in a plant script so the very next reading counts as out of range, running the script briefly, and then changing the value back once you have confirmed the alert arrived.
