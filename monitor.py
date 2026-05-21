import requests
import time

BOT_TOKEN = "8997355665:AAFdJsX52b6MDS1eF3jm-XXa3CCxs_L9Hmk"
CHAT_ID = "947121560"

SESSION_SID = "s%3AbNa3jfJs63Lat4WCqMoet8X7moV-r36n.olOLHB5ca3SWWLPi5tiCPvsI2rj0%2FeaIc6S9TWypY6U"
XSRF_TOKEN = "CpAASdjQ-0Z1BZSrcSaASlDbiPazP59tNQDA"

SEEN = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Cookie": f"respondent.session.sid={SESSION_SID}; XSRF-TOKEN={XSRF_TOKEN}",
    "Referer": "https://app.respondent.io/next/participants/projects?sort=publishedAt&eligible=true",
    "Accept": "application/json",
    "X-XSRF-TOKEN": XSRF_TOKEN
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
        print("Session may have expired.")
        return

    if r.text.strip().startswith("<"):
        print("Still returning HTML - session cookie needs refresh.")
        return

    try:
        data = r.json()
        projects = data.get("projects", data.get("data", []))
        print(f"Found {len(projects)} studies")
        for project in projects:
            title = project.get("title", project.get("name", ""))
            pid = project.get("_id", project.get("id", title))
            if title and pid not in SEEN:
                SEEN.add(pid)
                incentive = project.get("incentive", "N/A")
                duration = project.get("duration", "N/A")
                alert(
                    f"🆕 NEW STUDY ON RESPONDENT!\n\n"
                    f"📋 Study: {title}\n"
                    f"💰 Pay: {incentive}\n"
                    f"⏱ Duration: {duration}\n\n"
                    f"👉 Apply Now: {APPLY_URL}"
                )
    except Exception as e:
        print(f"Parse error: {e}")

alert("✅ Respondent Monitor STARTED! Checking every 60 seconds...")
print("Bot started. Monitoring every 60 seconds...")

while True:
    try:
        check()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(60)
