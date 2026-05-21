import requests
import time

BOT_TOKEN = "8997355665:AAFdJsX52b6MDS1eF3jm-XXa3CCxs_L9Hmk"
CHAT_ID = "947121560"
EMAIL = "barbragensley1141@outlook.com"
PASSWORD = "ayoboya1"
SEEN = set()
APPLY_URL = "https://app.respondent.io/next/participants/projects?sort=publishedAt&eligible=true"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://app.respondent.io",
    "Accept": "application/json",
    "Content-Type": "application/json"
})

def alert(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except Exception as e:
        print(f"Telegram error: {e}")

def login():
    print("Logging in...")
    r = session.post(
        "https://app.respondent.io/api/v2/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
        timeout=15
    )
    print(f"Login status: {r.status_code}")
    print(f"Login response: {r.text[:300]}")
    return r.status_code == 200

def check():
    r = session.get(
        "https://app.respondent.io/api/v2/projects?sort=publishedAt&eligible=true&limit=20",
        timeout=15
    )
    print(f"Status: {r.status_code} | Preview: {r.text[:100]}")

    if r.text.strip().startswith("<"):
        print("Session expired — re-logging in...")
        login()
        return

    data = r.json()
    projects = data.get("projects", data.get("data", []))
    print(f"Found {len(projects)} studies")

    for p in projects:
        title = p.get("title", p.get("name", ""))
        pid = p.get("_id", p.get("id", title))
        if title and pid not in SEEN:
            SEEN.add(pid)
            alert(
                f"🆕 NEW STUDY ON RESPONDENT!\n\n"
                f"📋 Study: {title}\n"
                f"💰 Pay: {p.get('incentive', 'N/A')}\n"
                f"⏱ Duration: {p.get('duration', 'N/A')}\n\n"
                f"👉 Apply: {APPLY_URL}"
            )

if login():
    alert("✅ Respondent Monitor STARTED with auto-login!")
    print("Bot started. Monitoring every 60 seconds...")
    while True:
        try:
            check()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)
else:
    print("Login failed. Check your email/password.")
    alert("❌ Respondent Monitor login failed. Check credentials.")
