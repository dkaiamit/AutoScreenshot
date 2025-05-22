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

async def take_screenshots(urls: List[str], session_id: str = None) -> List[str]:
    # Generate a session ID if not provided
    if session_id is None:
        session_id = str(uuid.uuid4())
        
    output_dir = os.path.join("screenshots", session_id)
    os.makedirs(output_dir, exist_ok=True)

    screenshots = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            for idx, url in enumerate(urls):
                try:
                    await page.goto(url, timeout=15000)
                    await page.wait_for_load_state("networkidle")
                    
                    screenshot_path = os.path.join(output_dir, f"screenshot_{idx+1}.png")
                    await page.screenshot(path=screenshot_path, full_page=True)
                    screenshots.append(screenshot_path)

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
