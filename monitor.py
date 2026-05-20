print("SCRIPT STARTED")

import os
import time
import requests
from ntscraper import Nitter  # X kısıtlamalarını aşmak için eklendi

# Çevre değişkenleri (Kendi bilgilerinizi işletim sistemine tanımlayın)
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
        # Nitter modülünü başlatıyoruz
        scraper = Nitter(log_level=0)
        
        # Kullanıcının profil bilgilerini çekmeye çalışıyoruz
        print(f"@{USERNAME} hesabı kontrol ediliyor...")
        profile = scraper.get_profile_info(USERNAME)
        
        # Eğer profil bilgisi başarıyla döndüyse ve boş değilse hesap aktiftir
        if profile and 'username' in profile:
            print("HESAP AKTİF (Profil başarıyla okundu)")
            return True
        else:
            print("HESAP PASİF (Profil bulunamadı veya askıda)")
            return False
            
    except Exception as e:
        # Hesap tamamen silindiğinde veya bulunamadığında kütüphane hata verecektir, 
        # bu durum hesabın pasif/kapalı olduğu anlamına gelir.
        print(f"HESAP BULUNAMADI VEYA PASİF. Detay: {e}")
        return False

print("BOT STARTED")
send_telegram("✅ BOT ONLINE - X Takip Sistemi Başlatıldı.")

# Durum değişimlerini takip etmek için ilk değer ataması (Sürekli aynı mesajı atmaması için)
last_status = None

while True:
    try:
        current_status = check_account()

        # Durum değiştiğinde veya ilk defa veri alındığında Telegram'a mesaj atar
        if current_status != last_status:
            if current_status:
                send_telegram(f"🟢 @{USERNAME} hesabı AKTİF.")
            else:
                send_telegram(f"🔴 @{USERNAME} hesabı PASİF (Kapandı, askıya alındı veya kullanıcı adı değişti).")
            
            # Güncel durumu kaydet
            last_status = current_status

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("ANA DÖNGÜ HATASI:", e)
        time.sleep(60)
