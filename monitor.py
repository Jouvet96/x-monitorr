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

        url = (
            f"https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendMessage"
        )

        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        r = requests.post(
            url,
            data=data,
            timeout=15
        )

        print(
            "TELEGRAM:",
            r.status_code
        )

    except Exception as e:

        print(
            "TELEGRAM ERROR:",
            e
        )


print("BOT STARTED")

send_telegram(
    "✅ BOT ONLINE"
)


while True:

    try:

        url = (
            f"https://x.com/"
            f"{USERNAME}"
        )

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

        text = r.text.lower()

        print(
            "HTTP:",
            r.status_code
        )

        # SADECE BUNU KONTROL ET
        if (
            "only confirmed followers can see"
            in text
        ):

            print(
                "ACCOUNT ACTIVE"
            )

            send_telegram(
                f"🟢 "
                f"@{USERNAME} "
                f"AKTİF"
            )

        else:

            print(
                "ACCOUNT PASSIVE"
            )

            send_telegram(
                f"🔴 "
                f"@{USERNAME} "
                f"PASİF"
            )

        time.sleep(
            CHECK_INTERVAL
        )

    except Exception as e:

        print(
            "MAIN LOOP ERROR:",
            e
        )

        time.sleep(60)
