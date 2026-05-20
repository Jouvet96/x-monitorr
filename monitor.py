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

    requests.post(url, data=data)


def is_suspended(username):
    url = f"https://x.com/{username}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    text = r.text.lower()

    return "account suspended" in text


print("BOT STARTED")

last_state = True

while True:
    try:
        suspended = is_suspended(USERNAME)

        print("CHECK:", suspended)

        if last_state and not suspended:
            send_telegram(
                f"🚨 @{USERNAME} hesabı aktif oldu!"
            )

        last_state = suspended

        time.sleep(30)

    except Exception as e:
        print(e)
        time.sleep(30)