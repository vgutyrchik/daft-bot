import os
import time
import requests
import re
import json

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SEARCH_URL = os.environ.get("SEARCH_URL")

sent_links = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram error:", e)

def extract_listings(html):
    listings = []

    # Ищем JSON внутри страницы
    match = re.search(r'window\.__PRELOADED_STATE__ = ({.*});', html)

    if not match:
        print("JSON not found")
        return listings

    try:
        data = json.loads(match.group(1))

        ads = data["search"]["results"]["ads"]

        for ad in ads:
            link = "https://www.daft.ie" + ad["seoFriendlyPath"]
            listings.append(link)

    except Exception as e:
        print("JSON parse error:", e)

    return listings

def check_daft(initial=False):

    try:
        r = requests.get(SEARCH_URL, headers=HEADERS)
    except Exception as e:
        print("Request error:", e)
        return

    if r.status_code != 200:
        print("Status code:", r.status_code)
        return

    listings = extract_listings(r.text)

    if not listings:
        print("No listings found")
        return

    for link in listings:

        if link not in sent_links:

            sent_links.add(link)

            prefix = "🏠 Current listing:" if initial else "🏠 New listing:"

            send_telegram(f"{prefix}\n{link}")

            print("Sent:", link)

print("Bot started")
send_telegram("✅ Bot started and monitoring Daft.ie")

# Отправить все текущие
check_daft(initial=True)

# Мониторинг новых
while True:

    check_daft()

    time.sleep(60)
