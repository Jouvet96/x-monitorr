print("SCRIPT STARTED")

import os
import time
import requests

USERNAME = os.getenv("USERNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECK_INTERVAL = 60


def send_telegram(message):

    try:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        r = requests.post(
            url,
            data=data,
            timeout=15
        )

        print("TELEGRAM:", r.status_code)

    except Exception as e:

        print("TELEGRAM ERROR:", e)


def check_account():

    try:

        url = f"https://x.com/{USERNAME}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        }

        r = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("HTTP STATUS:", r.status_code)

        text = r.text.lower()

        # aktif kontrolü
        if (
            "followers" in text
            and "following" in text
        ):

            print("ACCOUNT ACTIVE")

            return True

        else:

            print("ACCOUNT PASSIVE")

            return False

    except Exception as e:

        print("CHECK ERROR:", e)

        return False


print("BOT STARTED")

send_telegram("✅ BOT ONLINE")


while True:

    try:

        current_status = check_account()

        if current_status:

            send_telegram(
                f"🟢 @{USERNAME} hesabı AKTİF."
            )

        else:

            send_telegram(
                f"🔴 @{USERNAME} hesabı PASİF."
            )

        time.sleep(CHECK_INTERVAL)

    except Exception as e:

        print("MAIN LOOP ERROR:", e)

        time.sleep(60)
