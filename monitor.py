import requests
import time

BOT_TOKEN = "8997355665:AAFdJsX52b6MDS1eF3jm-XXa3CCxs_L9Hmk"
CHAT_ID = "947121560"
SEEN = set()
APPLY_URL = "https://app.respondent.io/next/participants/projects?sort=publishedAt&eligible=true"

# --- PASTE ALL YOUR COOKIES HERE AS ONE STRING ---
COOKIES = (
    "_csrf=nDNrSvOInf3fhvUDPj2URwLf; "
    "ajs_anonymous_id=afb1aa20-d783-4883-8b2e-8cd16a401650; "
    "ajs_user_id=6a0371a7e7ac41b1ede82a75; "
    "respondent.session.sid=s%3AbNa3jfJs63Lat4WCqMoet8X7moV-r36n.olOLHB5ca3SWWLPi5tiCPvsI2rj0%2FeaIc6S9TWypY6U; "
    "XSRF-TOKEN=CpAASdjQ-0Z1BZSrcSaASlDbiPazP59tNQDA; "
    "rio_cookie_consent=denied; "
    "intercom-device-id-mzi9ntpw=23641c24-bcb7-4326-9e6a-4bac1060ac01; "
    "intercom-id-mzi9ntpw=41795592-01bb-4904-b1bc-da36dcdbd6f2"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": COOKIES,
    "Referer": "https://app.respondent.io/next/participants/projects?sort=publishedAt&eligible=true",
    "Origin": "https://app.respondent.io",
    "X-XSRF-TOKEN": "CpAASdjQ-0Z1BZSrcSaASlDbiPazP59tNQDA",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124"',
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
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
    r = requests.get(
        "https://app.respondent.io/api/v2/projects?sort=publishedAt&eligible=true&limit=20",
        headers=HEADERS,
        timeout=15
    )
    print(f"Status: {r.status_code} | Preview: {r.text[:200]}")

    if r.text.strip().startswith("<"):
        alert("⚠️ Cookies expired! Please update monitor.py with fresh cookies.")
        print("HTML returned — cookies need refreshing.")
        time.sleep(3600)
        return

    data = r.json()
    projects = data.get("projects", data.get("data", []))
    print(f"✅ Found {len(projects)} studies")

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

alert("✅ Respondent Monitor STARTED!")
print("Bot started. Monitoring every 60 seconds...")
while True:
    try:
        check()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(60)
