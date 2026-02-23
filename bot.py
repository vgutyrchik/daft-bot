import os
import time
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

seen = set()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    
    requests.post(url, data=data)

def check_daft():
    url = "https://www.daft.ie/sharing/dublin"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return
    
    html = response.text
    
    lines = html.split('href="')
    
    for line in lines:
        if "/sharing/" in line:
            
            link = line.split('"')[0]
            full_link = "https://www.daft.ie" + link
            
            if full_link not in seen:
                
                seen.add(full_link)
                
                send_telegram("New room found:\n" + full_link)

send_telegram("✅ Bot started and test message")

while True:
    
    try:
        check_daft()
    except:
        pass
    
    time.sleep(60)
