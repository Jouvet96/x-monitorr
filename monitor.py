print("SCRIPT STARTED")

import os
import time
import requests

USERNAME = os.getenv("USERNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    r = requests.post(url, data=data)

    print("TELEGRAM:", r.status_code)


print("BOT STARTED")

send_telegram("✅ BOT ONLINE")


while True:

    try:

        print("LOOP WORKING")

        url = f"https://x.com/{USERNAME}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("HTTP:", r.status_code)

        text = r.text.lower()

        if "account suspended" in text:

            print("ACCOUNT SUSPENDED")

        elif "followers" in text:

            print("ACCOUNT ACTIVE")

        else:

            print("UNKNOWN PAGE")

        time.sleep(60)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(30)
