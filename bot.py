import os
import time
import requests
from bs4 import BeautifulSoup

# ====== Переменные ======
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SEARCH_URL = os.environ.get("SEARCH_URL")
COOKIE = os.environ.get("COOKIE")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": COOKIE
}

sent_links = set()  # Уже отправленные ссылки

# ====== Telegram ======
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

# ====== Парсер Daft ======
def get_listings():
    """Возвращает список ссылок текущих объявлений"""
    try:
        r = requests.get(SEARCH_URL, headers=HEADERS)
    except Exception as e:
        print("Request error:", e)
        return []

    if r.status_code != 200:
        print("Status code:", r.status_code)
        return []

    soup = BeautifulSoup(r.text, "lxml")
    articles = soup.find_all("article")

    links = []
    for art in articles:
        link_tag = art.find("a", href=True)
        if link_tag:
            link = "https://www.daft.ie" + link_tag['href']
            links.append(link)

    return links

def check_daft(initial=False):
    listings = get_listings()
    if not listings:
        print("No listings found")
        return

    new_found = False
    for link in listings:
        if link not in sent_links:
            sent_links.add(link)
            prefix = "🏠 Current listing:" if initial else "🏠 New listing:"
            send_telegram(f"{prefix}\n{link}")
            new_found = True

    if not new_found and not initial:
        print("No new listings")

# ====== Главный цикл ======
print("Bot started")
send_telegram("✅ Bot started and monitoring Daft.ie")

# Сначала пришлём все существующие объявления
check_daft(initial=True)

# Затем мониторим новые
while True:
    check_daft()
