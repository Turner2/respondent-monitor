import requests
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "8997355665:AAFdJsX52b6MDS1eF3jm-XXa3CCxs_L9Hmk"
CHAT_ID = "947121560"
SESSION_SID = "s%3AOdu33_IFUNJ07-6rcorL5_d2jw00qy7-.nh%2Bj9JRkBFSFl5ktHNcveZqb0FU67Xfhqdkh2o6C%2Bsw"
CSRF_TOKEN = "nDNrSvOInf3fhvUDPj2URwLf"
SEEN = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Cookie": f"respondent.session.sid={SESSION_SID}; _csrf={CSRF_TOKEN}",
    "Referer": "https://app.respondent.io"
}

URL = "https://app.respondent.io/next/participants/projects?sort=publishedAt&eligible=true"

def alert(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print(f"Telegram error: {e}")

def check():
    r = requests.get(URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.find_all("h2")
    for t in titles:
        text = t.get_text(strip=True)
        if text and text not in SEEN:
            SEEN.add(text)
            alert(
                f"🔔 <b>NEW STUDY ON RESPONDENT!</b>\n\n"
                f"📋 <b>{text}</b>\n\n"
                f"🔗 <a href=\"{URL}\">Click Here to Apply Now</a>"
            )

alert("✅ <b>Respondent Monitor is LIVE!</b>\n\n🔍 Checking every 60 seconds.\n🔔 You'll be alerted the moment a new study appears!")

print("Bot started. Monitoring every 60 seconds...")

while True:
    try:
        check()
    except Exception as e:
        print(f"Error: {e}")
        alert(f"⚠️ Error: {e}\nRetrying in 60 seconds.")
    time.sleep(60)
