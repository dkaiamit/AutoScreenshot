from fastapi import FastAPI
from pydantic import BaseModel
import base64
import uuid
import os

app = FastAPI()

class ScreenshotUpload(BaseModel):
    email: str
    password: str
    serial: int
    image: str  # Base64 encoded PNG

@app.post("/upload_screenshot")
async def upload_screenshot(payload: ScreenshotUpload):
    try:
        session_id = str(uuid.uuid4())
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/screenshot_{session_id}.png"

        header = "data:image/png;base64,"
        image_data = payload.image
        if image_data.startswith(header):
            image_data = image_data[len(header):]

        with open(screenshot_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        return {"status": "success", "file": screenshot_path}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
