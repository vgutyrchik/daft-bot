import requests
import time
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SEARCH_URL = os.environ.get("SEARCH_URL")
COOKIE = os.environ.get("COOKIE")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": COOKIE
}

sent_links = set()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    }
    requests.post(url, data=data)

def check_daft():
    print("Checking Daft...")
    
    response = requests.get(SEARCH_URL, headers=HEADERS)
    
    if response.status_code != 200:
        print("Error:", response.status_code)
        return
    
    html = response.text
    
    parts = html.split('/sharing/')
    
    new_found = False
    
    for part in parts[1:6]:
        link = "https://www.daft.ie/sharing/" + part.split('"')[0]
        
        if link not in sent_links:
            sent_links.add(link)
            send_telegram(f"🏠 New listing:\n{link}")
            new_found = True
    
    if not new_found:
        print("No new listings")

print("Bot started")
send_telegram("✅ Bot started and monitoring Daft.ie")

while True:
    try:
        check_daft()
    except Exception as e:
        print("Error:", e)
    
    time.sleep(60)
