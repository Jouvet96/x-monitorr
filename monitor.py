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
        response = requests.post(
            url,
            data=data,
            timeout=15
        )

        print("Telegram:", response.status_code)

    except Exception as e:
        print("Telegram error:", e)


def is_account_active(username):
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

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        text = response.text.lower()

        print("HTTP:", response.status_code)

        # suspend kontrolü
        if "account suspended" in text:
            print("STATUS: suspended")
            return False

        # kullanıcı yoksa
        if "this account doesn" in text:
            print("STATUS: account not found")
            return False

        # x blokladıysa
        blocked_words = [
            "rate limit exceeded",
            "something went wrong",
            "log in to x",
            "sign in to x",
            "enter your phone number",
            "unusual traffic"
        ]

        for word in blocked_words:
            if word in text:
                print("STATUS: blocked by x")
                return None

        # profil işaretleri
        profile_words = [
            "followers",
            "following",
            "joined",
            "posts"
        ]

        for word in profile_words:
            if word in text:
                print("STATUS: active")
                return True

        print("STATUS: unknown")
        return None

    except Exception as e:
        print("Check error:", e)
        return None


print("BOT STARTED")

# ilk durum
last_status = is_account_active(USERNAME)

print("Initial status:", last_status)

while True:
    try:
        current_status = is_account_active(USERNAME)

        print("Current status:", current_status)

        # sadece gerçekten suspend -> active geçişinde bildir
        if (
            last_status is False
            and current_status is True
        ):
            msg = (
                f"🚨 @{USERNAME} hesabı aktif oldu!"
            )

            print(msg)

            send_telegram(msg)

        # sadece geçerli sonuç varsa güncelle
        if current_status is not None:
            last_status = current_status

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("MAIN LOOP ERROR:", e)
        time.sleep(60)
