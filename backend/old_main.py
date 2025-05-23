# main.py

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
import asyncio

# Our custom modules (we'll build these later)
from screenshot import take_screenshots
# from sharepoint_upload import upload_to_sharepoint
# from email_notify import send_email_notification

app = FastAPI()

# Enable CORS so Chrome extension can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model for screenshot request
class ScreenshotRequest(BaseModel):
    urls: List[str]
    username: str
    password: str
    email: str

app = FastAPI()

@app.get("/test-screenshot")
async def test_screenshot():
    urls = ["https://example.com", "https://httpbin.org/html"]
    screenshots = await take_screenshots(urls)
    return {"status": "ok", "files": screenshots}

@app.get("/")
async def root():
    return {"message": "Backend is up and running"}

# POST endpoint triggered by Chrome extension
@app.post("/process/")
async def process_screenshots(data: ScreenshotRequest):
    """
    1. Takes a list of URLs + login info from user
    2. Screenshots them using headless browser
    3. Uploads to SharePoint
    4. Sends an email to user with links
    """
    try:
        session_id = str(uuid.uuid4())  # unique session for logging

        # 1. Take screenshots (returns list of local file paths)
        screenshots = await take_screenshots(data.urls, data.username, data.password, session_id)

        # 2. Upload to SharePoint (returns list of URLs)
        # sharepoint_links = await upload_to_sharepoint(screenshots, session_id)

        # # 3. Send email with links
        # await send_email_notification(data.email, sharepoint_links)

        # return {"status": "success", "links": sharepoint_links}
        return {
            "status": "success",
            "screenshots": screenshots,
            "message": "Screenshots captured successfully"
                }


    except Exception as e:
        return {"status": "error", "detail": str(e)}
