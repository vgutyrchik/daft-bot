import os
import time
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

sent_ids = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

API_URL = "https://gateway.daft.ie/old/v1/search"

PARAMS = {
    "location": "dublin-city",
    "adType": "sharing",
    "maxPrice": "900",
    "sort": "publishDateDesc",
    "from": "0",
    "size": "20"
}

def send_telegram(text):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

def check_daft(initial=False):

    try:

        r = requests.get(API_URL, headers=HEADERS, params=PARAMS)

        if r.status_code != 200:

            print("API status:", r.status_code)
            return

        data = r.json()

        listings = data.get("results", [])

        for listing in listings:

            ad_id = listing.get("adId")

            if ad_id in sent_ids:
                continue

            sent_ids.add(ad_id)

            link = f"https://www.daft.ie/sharing/{ad_id}"

            prefix = "🏠 Current listing:" if initial else "🏠 New listing:"

            send_telegram(f"{prefix}\n{link}")

            print("Sent:", link)

    except Exception as e:

        print("Error:", e)

print("Bot started")

send_telegram("✅ Bot started and monitoring Daft.ie")

check_daft(initial=True)

while True:

    check_daft()

    time.sleep(60)
