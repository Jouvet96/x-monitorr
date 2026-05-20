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

        print("TELEGRAM STATUS:", r.status_code)

    except Exception as e:
        print("TELEGRAM ERROR:", e)


def check_account(username):
    try:
        url = f"https://x.com/{username}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        }

        r = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("HTTP STATUS:", r.status_code)

        text = r.text.lower()

        # suspended
        if "account suspended" in text:
            print("ACCOUNT SUSPENDED")
            return False

        # account not found
        if "this account doesn" in text:
            print("ACCOUNT NOT FOUND")
            return False

        # x blocked request
        blocked = [
            "rate limit exceeded",
            "something went wrong",
            "log in to x",
            "sign in to x",
            "unusual traffic"
        ]

        for word in blocked:
            if word in text:
                print("X BLOCKED REQUEST")
                return None

        # active profile indicators
        indicators = [
            "followers",
            "following",
            "joined",
            "posts"
        ]

        for word in indicators:
            if word in text:
                print("ACCOUNT ACTIVE")
                return True

        print("UNKNOWN PAGE")
        return None

    except Exception as e:
        print("CHECK ERROR:", e)
        return None


print("BOT STARTED")

send_telegram("✅ Bot aktif.")

last_status = check_account(USERNAME)

print("INITIAL STATUS:", last_status)

while True:

    try:
        print("CHECKING ACCOUNT...")

        current_status = check_account(USERNAME)

        print("CURRENT STATUS:", current_status)

        # suspended -> active
        if (
            last_status is False
            and current_status is True
        ):
            send_telegram(
                f"🚨 @{USERNAME} hesabı aktif oldu!"
            )

        # update only valid states
        if current_status is not None:
            last_status = current_status

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("MAIN LOOP ERROR:", e)
        time.sleep(60)
