import os
import time
from playwright.sync_api import sync_playwright
import requests

# Mengambil konfigurasi rahasia dari GitHub Secrets (jika ada)
TELEGRAM_BOT_TOKEN = os.getenv("8825056246:AAGuXgQRyv4KEoUsseOK6-Hj-SprOwxfgjU")
TELEGRAM_CHAT_ID = os.getenv("T8279395377")

def send_telegram_message(message):
    """Fungsi untuk mengirim laporan hasil analisis ke Telegram"""
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Gagal mengirim pesan Telegram: {e}")

def run_scraper():
    print("🚀 Bot mulai berjalan di server GitHub Actions...")
    
    with sync_playwright() as p:
        # Menjalankan Chromium di server Linux Ubuntu (100% aman & lancar)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Ganti dengan URL target data/history yang ingin dipantau
            target_url = "https://example.com" 
            page.goto(target_url, timeout=60000)
            page.wait_for_timeout(3000)
            
            # Contoh mengambil teks dari elemen web target
            # Sesuaikan '.crash-history-item' dengan selector web aslinya nanti
            elements = page.locator(".crash-history-item").all_inner_texts()
            
            print(f"📊 Berhasil mengambil {len(elements)} data mentah.")
            
            # Simulasi pengolahan data statistik sederhana
            multipliers = []
            for item in elements:
                try:
                    val = float(item.replace('x', '').strip())
                    multipliers.append(val)
                except ValueError:
                    continue
            
            # Format laporan hasil
            report = (
                f"🤖 *LAPORAN ANALISIS BOT SPACEMAN*\n\n"
                f"📈 Status: Berjalan Otomatis\n"
                f"🟢 Server: Linux GitHub Actions\n"
                f"⚡ Proses Selesai Sukses!"
            )
            
            print(report)
            send_telegram_message(report)
            
        except Exception as e:
            err_msg = f"❌ Error saat eksekusi: {str(e)}"
            print(err_msg)
            send_telegram_message(err_msg)
            
        finally:
            browser.close()

if __name__ == "__main__":
    run_scraper()
