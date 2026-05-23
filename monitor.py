import os
import time
import requests
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("USERNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECK_INTERVAL = 60
last_status = None


def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        r = requests.post(url, data=data, timeout=15)
        print("TELEGRAM:", r.status_code)
    except Exception as e:
        print("TELEGRAM ERROR:", e)


def check_account():
    url = f"https://x.com/{USERNAME}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])

        page = browser.new_page(
            locale="tr-TR",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            ),
            extra_http_headers={
                "Accept-Language": "tr-TR,tr;q=0.9"
            }
        )

        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(8000)

        text = page.inner_text("body").lower()

        print("PAGE TEXT:")
        print(text[:1000])

        browser.close()

        if "gönderilerini yalnızca onaylı takipçileri görebilir" in text:
            return True

        return False


print("BOT STARTED")
send_telegram("✅ BOT ONLINE")

while True:
    try:
        current_status = check_account()

        print("CURRENT STATUS:", current_status)
        print("LAST STATUS:", last_status)

        if current_status != last_status:
            if current_status is True:
                send_telegram(f"🟢 @{USERNAME} AKTİF")
            else:
                send_telegram(f"🔴 @{USERNAME} PASİF")

            last_status = current_status
        else:
            print("Durum değişmedi, mesaj gönderilmedi.")

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("MAIN ERROR:", e)
        send_telegram(f"⚠️ Kontrol hatası: {e}")
        time.sleep(60)
