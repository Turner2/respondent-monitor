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

IGNORE = {
    "available projects", "share respondent", "no projects available",
    "eligible projects", "all projects", "projects", ""
}

def alert(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except Exception as e:
        print(f"Telegram error: {e}")

def check():
    r = requests.get(URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    studies = (
        soup.find_all("h3") or
        soup.find_all("a", class_=lambda x: x and "project" in x.lower()) or
        soup.find_all("div", class_=lambda x: x and "title" in x.lower())
    )

    for t in studies:
        text = t.get_text(strip=True)
        if text and text.lower() not in IGNORE and text not in SEEN and len(text) > 10:
            SEEN.add(text)
            alert(
                f"NEW STUDY ON RESPONDENT!\n\n"
                f"Study: {text}\n\n"
                f"Apply Now: {URL}"
            )

alert("Respondent Monitor UPDATED & LIVE! Now detecting real study names. Checking every 60 seconds.")

print("Bot started. Monitoring every 60 seconds...")

while True:
    try:
        check()
    except Exception as e:
        print(f"Error: {e}")
        alert(f"Error: {e} Retrying in 60 seconds.")
    time.sleep(60)
