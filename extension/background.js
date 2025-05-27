chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.type === "scrolling_screenshot") {
    chrome.tabs.captureVisibleTab(null, { format: "png" }, async (base64Image) => {
      if (chrome.runtime.lastError) {
        sendResponse({ success: false, error: chrome.runtime.lastError.message });
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/upload_screenshot", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: message.email,
            password: message.password,
            serial: 0,
            image: base64Image
          })
        });
        const data = await response.json();
        sendResponse({ success: true, data });
      } catch (error) {
        sendResponse({ success: false, error: error.message });
      }
    });

    return true; // indicates async response
  }
});
