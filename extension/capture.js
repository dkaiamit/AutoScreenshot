(async () => {
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "capture_and_upload") {
      const { email, password } = message;

      const countdown = 15;
      const overlay = document.createElement("div");
      overlay.style.position = "fixed";
      overlay.style.top = 0;
      overlay.style.left = 0;
      overlay.style.width = "100vw";
      overlay.style.height = "100vh";
      overlay.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
      overlay.style.color = "white";
      overlay.style.fontSize = "30px";
      overlay.style.zIndex = 10000;
      overlay.style.display = "flex";
      overlay.style.justifyContent = "center";
      overlay.style.alignItems = "center";

      document.body.appendChild(overlay);
      let remaining = countdown;

      const interval = setInterval(() => {
        overlay.textContent = `Login & MFA expected. Capturing screenshot in ${remaining} seconds...`;
        remaining--;
        if (remaining < 0) {
          clearInterval(interval);
          document.body.removeChild(overlay);
          captureScrollingScreenshot();
        }
      }, 1000);

      function captureScrollingScreenshot() {
        chrome.runtime.sendMessage({ type: "scrolling_screenshot", email, password }, (response) => {
          console.log("Screenshot result:", response);
        });
      }
    }
  });
})();
