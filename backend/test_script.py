# test_script.py

import asyncio
from screenshot import take_screenshots

async def run():
    urls = ["https://example.com"]
    screenshots = await take_screenshots(urls)
    print(screenshots)

asyncio.run(run())
