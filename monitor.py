import asyncio
import requests
from playwright.async_api import async_playwright

BOT_TOKEN = "8997355665:AAFdJsX52b6MDS1eF3jm-XXa3CCxs_L9Hmk"
CHAT_ID = "947121560"
EMAIL = "barbragensley1141@outlook.com"
PASSWORD = "ayoboya1"
SEEN = set()
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

async def monitor():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("Logging in...")
        await page.goto("https://app.respondent.io/login", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        await page.fill('input[type="email"]', EMAIL)
        await page.fill('input[type="password"]', PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(8000)

        print(f"After login URL: {page.url}")

        if "login" in page.url.lower():
            print("Login failed.")
            alert("❌ Respondent login failed.")
            await browser.close()
            return

        alert("✅ Respondent monitor started.")
        print("Logged in. Monitoring every 60 seconds...")

        while True:
            try:
                await page.goto(APPLY_URL, wait_until="domcontentloaded")
                await page.wait_for_timeout(5000)

                titles = await page.eval_on_selector_all(
                    "h1, h2, h3, h4, [class*='title']",
                    """els => els
                        .map(e => e.innerText.trim())
                        .filter(t => t && t.length > 12)"""
                )

                print(f"Found {len(titles)} possible titles")

                for title in titles:
                    if title not in SEEN:
                        SEEN.add(title)
                        alert(f"🆕 NEW RESPONDENT ITEM\\n\\n{title}\\n\\n{APPLY_URL}")

            except Exception as e:
                print(f"Check error: {e}")

            await asyncio.sleep(60)

asyncio.run(monitor())
