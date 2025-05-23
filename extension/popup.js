document.getElementById("screenshotForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const serial = document.getElementById("serial").value;

  // Map serial to a predefined URL
  const serialToUrl = {
    "1": "https://google.com",
    "2": "https://linkedin.com",
    // add more mappings
  };

  const targetUrl = serialToUrl[serial];

  if (!targetUrl) {
    alert("Invalid serial number.");
    return;
  }

  // Send POST request to FastAPI backend
  try {
    const response = await fetch("http://localhost:8000/screenshot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        urls: [targetUrl],
        username: email,
        password: password,
        email: email
      })
    });

    const result = await response.json();
    console.log("Response:", result);

    if (result.status === "success") {
      alert("Screenshot taken successfully.");
    } else {
      alert("Error: " + result.detail);
    }
  } catch (err) {
    alert("Failed to reach backend: " + err.message);
  }
});
