import requests
import time
import json

BOT_TOKEN = "8997355665:AAFdJsX52b6MDS1eF3jm-XXa3CCxs_L9Hmk"
CHAT_ID = "947121560"
SESSION_SID = "s%3AOdu33_IFUNJ07-6rcorL5_d2jw00qy7-.nh%2Bj9JRkBFSFl5ktHNcveZqb0FU67Xfhqdkh2o6C%2Bsw"
CSRF_TOKEN = "nDNrSvOInf3fhvUDPj2URwLf"
SEEN = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Cookie": f"respondent.session.sid={SESSION_SID}; _csrf={CSRF_TOKEN}",
    "Referer": "https://app.respondent.io",
    "Accept": "application/json",
    "X-CSRF-Token": CSRF_TOKEN
}

API_URL = "https://app.respondent.io/api/v2/projects?sort=publishedAt&eligible=true&limit=20"
APPLY_URL = "https://app.respondent.io/next/participants/projects?sort=publishedAt&eligible=true"

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
    r = requests.get(API_URL, headers=HEADERS, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response preview: {r.text[:300]}")
    
    if r.status_code != 200:
        print("Session may have expired. Update your cookies.")
        return

    try:
        data = r.json()
        projects = data.get("projects", data.get("data", []))
        for project in projects:
            title = project.get("title", project.get("name", ""))
            pid = project.get("_id", project.get("id", title))
            if title and pid not in SEEN:
                SEEN.add(pid)
                incentive = project.get("incentive", "")
                duration = project.get("duration", "")
                alert(
                    f"NEW STUDY ON RESPONDENT!\n\n"
                    f"Study: {title}\n"
                    f"Pay: {incentive}\n"
                    f"Duration: {duration}\n\n"
                    f"Apply Now: {APPLY_URL}"
                )
    except Exception as e:
        print(f"Parse error: {e}")
        print(r.text[:500])

alert("Respondent Monitor RESTARTED with API method! Checking every 60 seconds.")
print("Bot started. Monitoring every 60 seconds...")

while True:
    try:
        check()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(60)
