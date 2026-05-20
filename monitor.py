import os
import time
import requests
from playwright.sync_api import sync_playwright

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
        r = requests.post(url, data=data, timeout=15)
        print("TELEGRAM:", r.status_code)
    except Exception as e:
        print("TELEGRAM ERROR:", e)


def check_account():
    url = f"https://x.com/{USERNAME}"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        )

        page.goto(url, wait_until="networkidle", timeout=60000)

        text = page.inner_text("body").lower()

        browser.close()

        print("PAGE TEXT:")
        print(text[:1000])

        if "only confirmed followers can see" in text:
            return True

        return False


print("BOT STARTED")
send_telegram("✅ BOT ONLINE")

while True:
    try:
        active = check_account()

        if active:
            print("ACCOUNT ACTIVE")
            send_telegram(f"🟢 @{USERNAME} AKTİF")
        else:
            print("ACCOUNT PASSIVE")
            send_telegram(f"🔴 @{USERNAME} PASİF")

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("MAIN ERROR:", e)
        send_telegram(f"⚠️ Kontrol hatası: {e}")
        time.sleep(60)
