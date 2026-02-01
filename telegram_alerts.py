# telegram_alerts.py

import urllib.request
import urllib.parse
import ssl

from settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(message):
    try:
        context = ssl._create_unverified_context()

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        data = urllib.parse.urlencode({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }).encode()

        req = urllib.request.Request(url, data=data)

        with urllib.request.urlopen(req, context=context, timeout=10):
            pass

        print("✅ SIGNAL SENT")

    except Exception as e:
        print(f"TELEGRAM ERROR: {e}")