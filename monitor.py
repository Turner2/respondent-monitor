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
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("Logging in...")
        await page.goto("https://app.respondent.io/login", wait_until="networkidle")
        await page.fill('input[type="email"]', EMAIL)
        await page.fill('input[type="password"]', PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(5000)

        url = page.url
        print(f"After login URL: {url}")

        if "login" in url:
            print("Login failed — check credentials or page structure")
            alert("❌ Respondent login failed. Check credentials.")
            await browser.close()
            return

        alert("✅ Respondent Monitor STARTED (Playwright)! Checking every 60s...")
        print("Logged in! Monitoring every 60 seconds...")

        while True:
            try:
                await page.goto(APPLY_URL, wait_until="networkidle")
                await page.wait_for_timeout(3000)

                content = await page.content()
                print(f"Page loaded. Length: {len(content)}")

                # Extract study titles from page
                titles = await page.eval_on_selector_all(
                    "h2, h3, [class*='title'], [class*='project'], [class*='study']",
                    "els => els.map(e => e.innerText.trim()).filter(t => t.length > 5)"
                )

                print(f"Found {len(titles)} potential studies: {titles[:3]}")

                for title in titles:
                    if title not in SEEN and len(title) > 10:
                        SEEN.add(title)
                        alert(
                            f"🆕 NEW STUDY ON RESPONDENT!\n\n"
                            f"📋 {title}\n\n"
                            f"👉 Apply: {APPLY_URL}"
                        )

            except Exception as e:
                print(f"Check error: {e}")

            await asyncio.sleep(60)

        await browser.close()

asyncio.run(monitor())
