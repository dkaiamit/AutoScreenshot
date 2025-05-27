document.getElementById("submit").addEventListener("click", async () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const serial = parseInt(document.getElementById("serial").value) - 1; // 0-based index

  chrome.tabs.query({}, async (tabs) => {
    if (serial < 0 || serial >= tabs.length) {
      alert("Invalid tab serial number");
      return;
    }

    const targetTab = tabs[serial];

    chrome.scripting.executeScript({
      target: { tabId: targetTab.id },
      files: ["capture.js"]
    }, () => {
      chrome.tabs.sendMessage(targetTab.id, {
        action: "capture_and_upload",
        email,
        password
      });
    });
  });
});
