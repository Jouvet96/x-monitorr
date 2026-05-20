print("SCRIPT STARTED")

import os
import time
import requests

USERNAME = os.getenv("USERNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECK_INTERVAL = 60  # Kontrol sıklığı (saniye)

def send_telegram(message):
    try:
        url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }
        r = requests.post(url, data=data, timeout=15)
        print("TELEGRAM DURUMU:", r.status_code)
    except Exception as e:
        print("TELEGRAM HATASI:", e)

def check_account():
    try:
        url = f"https://x.com/{USERNAME}"
        
        # Gerçek bir tarayıcı gibi görünmek için başlıklar
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }

        # allow_redirects=False yapıyoruz ki yönlendirmeleri kendimiz yakalayalım
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=False)
        
        print(f"X Yanıt Kodu (Status): {r.status_code}")

        # 1. DURUM: Hesap askıda, silinmiş veya yoksa X doğrudan 404 hatası verir.
        if r.status_code == 404:
            print("HESAP PASİF (404 - Bulunamadı veya Askıda)")
            return False

        # 2. DURUM: Hesap aktifse X bizi giriş ekranına yönlendirir (302) veya sayfayı açar (200).
        elif r.status_code in [200, 302]:
            # Eğer 302 ile yönlendiriyorsa, nereye yönlendirdiğine bakıyoruz
            redirect_url = r.headers.get("Location", "").lower()
            
            # Eğer yönlendirilen adres 'account/suspended' (askıya alındı) içeriyorsa pasiftir
            if "suspended" in redirect_url:
                print("HESAP PASİF (Askıya alınmış)")
                return False
                
            print("HESAP AKTİF (Giriş duvarına veya profile ulaşıldı)")
            return True

        else:
            # X botu engellediyse (Örn: 429 Too Many Requests) durumu bozmamak için eski kararı korumak en iyisidir
            print(t"Bilinmeyen yanıt kodu veya bot engeli: {r.status_code}")
            return None

    except Exception as e:
        print("KONTROL HATASI:", e)
        return None

print("BOT STARTED")
send_telegram("✅ BOT ONLINE - Kesin Durum Takibi Başlatıldı.")

last_status = None

while True:
    try:
        current_status = check_account()

        # Eğer gelen yanıt None ise (bağlantı hatası veya bot engeli), durumu değiştirme
        if current_status is not None and current_status != last_status:
            if current_status:
                send_telegram(f"🟢 @{USERNAME} hesabı AKTİF.")
            else:
                send_telegram(f"🔴 @{USERNAME} hesabı PASİF (Kapandı veya askıya alındı).")
            
            last_status = current_status

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("ANA DÖNGÜ HATASI:", e)
        time.sleep(60)
