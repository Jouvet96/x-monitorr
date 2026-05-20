print("SCRIPT STARTED")

import os
import time
import requests

USERNAME = os.getenv("USERNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECK_INTERVAL = 60

last_status = None


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
            timeout=20,
            allow_redirects=True
        )

        final_url = r.url.lower()

        print("FINAL URL:", final_url)

        # kullanıcı adına yönleniyorsa aktif say
        if USERNAME.lower() in final_url:
            return True

        return False

    except Exception as e:

        print("CHECK ERROR:", e)

        return False


print("BOT STARTED")

send_telegram("✅ BOT ONLINE")


while True:

    try:

        current_status = check_account()

        print("CURRENT STATUS:", current_status)

        # AKTİF
        if current_status:

            send_telegram(
                f"🟢 @{USERNAME} hesabı AKTİF."
            )

        # PASİF OLDU
        else:

            if last_status is True:

                send_telegram(
                    f"🔴 @{USERNAME} hesabı PASİF oldu."
                )

        last_status = current_status

        time.sleep(CHECK_INTERVAL)

    except Exception as e:

        print("MAIN LOOP ERROR:", e)

        time.sleep(60)
