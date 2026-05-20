print("SCRIPT STARTED")

import os
import time
import requests

USERNAME = os.getenv("USERNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECK_INTERVAL = 60


def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:

        r = requests.post(
            url,
            data=data,
            timeout=15
        )

        print("TELEGRAM:", r.status_code)

    except Exception as e:

        print("TELEGRAM ERROR:", e)


print("BOT STARTED")

send_telegram("✅ BOT ONLINE")


while True:

    try:

        print("CHECKING ACCOUNT...")

        url = f"https://x.com/{USERNAME}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("HTTP STATUS:", r.status_code)

        text = r.text.lower()

        # suspended kontrolü
        if "account suspended" in text:

            print("ACCOUNT SUSPENDED")

        # aktif profil kontrolü
        elif (
            "followers" in text
            or "following" in text
            or "posts" in text
        ):

            print("ACCOUNT ACTIVE")

            send_telegram(
                f"🚨 @{USERNAME} hesabı AKTİF görünüyor!"
            )

        else:

            print("UNKNOWN PAGE")

        time.sleep(CHECK_INTERVAL)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(60)
