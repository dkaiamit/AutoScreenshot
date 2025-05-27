# screenshot.py
# _______TESTING CODE__________
# screenshot.py

# screenshot.py

# screenshot.py

# screenshot.py

import os
from typing import List
from playwright.async_api import async_playwright
import uuid
import asyncio

async def take_screenshots(
    urls: List[str], username: str, password: str, email: str, session_id: str = None
) -> List[str]:
    if session_id is None:
        session_id = str(uuid.uuid4())
        
    output_dir = os.path.join("screenshots", session_id)
    os.makedirs(output_dir, exist_ok=True)

    screenshots = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # Use headless=False for testing
            context = await browser.new_context()
            page = await context.new_page()

            for idx, url in enumerate(urls):
                try:
                    print(f"[INFO] Navigating to: {url}")
                    await page.goto(url, timeout=15000)
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(15)  # Wait for MFA to complete
                    # Simulated login logic (form detection must be tailored to actual sites)
                    # You'll need to customize the selectors per real website
                    try:
                        await page.fill('input[type="email"], input[name="username"]', username)
                        await page.fill('input[type="password"]', password)
                        await page.click('button[type="submit"], input[type="submit"]')
                        print("[INFO] Credentials submitted.")
                    except Exception as login_e:
                        print(f"[WARN] Could not fill login form on {url}: {login_e}")

                    # Wait for user to complete MFA manually
                    print("[INFO] Waiting 15 seconds for MFA verification...")
                    await asyncio.sleep(15)

                    # Wait for page to settle post-MFA
                    await page.wait_for_load_state("networkidle", timeout=10000)

                    screenshot_path = os.path.join(output_dir, f"screenshot_{idx+1}.png")
                    await page.screenshot(path=screenshot_path, full_page=True)
                    screenshots.append(screenshot_path)

                    print(f"[SUCCESS] Screenshot saved: {screenshot_path}")

                except Exception as e:
                    print(f"[ERROR] Failed to process URL {url}: {e}")

            await browser.close()

    except Exception as e:
        import traceback
        print(f"[CRITICAL] Playwright launch failed:\n{traceback.format_exc()}")

    return screenshots




# ________ACTUAL CODE__________
# import os
# from playwright.async_api import async_playwright
# from typing import List

# async def take_screenshots(urls: List[str], username: str, password: str, session_id: str) -> List[str]:
#     output_dir = f"screenshots/{session_id}"
#     os.makedirs(output_dir, exist_ok=True)
#     screenshots = []

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context()

#         page = await context.new_page()

#         # LOGIN STEP (adjust based on your login page structure)
#         await page.goto(urls[0])

#         # Replace these selectors with your target site’s login form selectors
#         await page.fill('input[name="email"]', username)
#         await page.fill('input[name="password"]', password)
#         await page.click('button[type="submit"]')

#         # Wait for login to complete - change this as needed
#         await page.wait_for_load_state('networkidle')

#         for i, url in enumerate(urls):
#             await page.goto(url)
#             await page.wait_for_load_state('networkidle')

#             screenshot_path = f"{output_dir}/screenshot_{i+1}.png"
#             await page.screenshot(path=screenshot_path, full_page=True)
#             screenshots.append(screenshot_path)

#         await browser.close()

#     return screenshots
