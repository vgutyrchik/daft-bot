import requests
import time
import telegram

BOT_TOKEN = "8202785705:AAFbclnPKtYfWD89bGQZwII_O15E4ZtnjLc"
CHAT_ID = "588443934"

bot = telegram.Bot(token=BOT_TOKEN)

URL = "https://gateway.daft.ie/old/v1/listings"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Origin": "https://www.daft.ie",
    "Referer": "https://www.daft.ie/"
}

PARAMS = {
    "location": "dublin-city",
    "maxRent": 900,
    "sort": "publishDateDesc",
    "offset": 0,
    "limit": 20
}

seen = set()

def check():
    try:
        r = requests.get(URL, headers=HEADERS, params=PARAMS)

        print("Status:", r.status_code)

        if r.status_code != 200:
            return

        data = r.json()

        listings = data.get("listings", [])

        for listing in listings:

            id = listing.get("id")

            if id in seen:
                continue

            seen.add(id)

            title = listing.get("title")
            link = f"https://www.daft.ie{listing.get('seoFriendlyPath')}"

            message = f"{title}\n{link}"

            bot.send_message(CHAT_ID, message)

    except Exception as e:
        print(e)


print("Bot started")

while True:
    check()
    time.sleep(60)
