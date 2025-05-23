const websiteMap = {
  "1": "https://example.com",
  "2": "https://login.example2.com"
  // add more based on serial
};

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "TRIGGER_SCREENSHOT") {
    const { email, password, serial } = msg;
    const url = websiteMap[serial];

    if (!url) {
      console.error("Invalid serial number");
      return;
    }

    chrome.tabs.create({ url }, (tab) => {
      setTimeout(() => {
        // After 15 seconds delay for MFA, send POST to backend
        fetch("http://localhost:8000/screenshot-login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            urls: [url],
            username: email,
            password: password,
            email: email
          })
        }).then(res => res.json()).then(data => {
          console.log("Screenshot taken:", data);
        });
      }, 15000); // 15 seconds wait for MFA
    });
  }
});
