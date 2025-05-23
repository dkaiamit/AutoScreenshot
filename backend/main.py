from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from screenshot import take_screenshots  # Ensure this is implemented correctly

app = FastAPI()

# Input schema based on frontend payload
class ScreenshotRequest(BaseModel):
    urls: List[str]       # URLs to capture (sent from popup.js)
    username: str         # Email used for login (from popup)
    password: str         # Password used for login
    email: str            # Also email (used later to send SharePoint link)

@app.post("/screenshot")
async def capture_screenshot(payload: ScreenshotRequest):
    try:
        await take_screenshots(
            urls=payload.urls,
            username=payload.username,
            password=payload.password,
            email=payload.email
        )
        return {"status": "success"}
    
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": "error",
            "detail": str(e)
        })
