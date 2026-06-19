const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const statusText = document.getElementById("status");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

const registerBtn = document.getElementById("registerBtn");
const verifyBtn = document.getElementById("verifyBtn");

const toast = document.getElementById("toast");

// ✅ toast popup
function showToast(message, type = "success") {
  toast.className = `toast show ${type}`;
  toast.innerText = message;

  setTimeout(() => {
    toast.className = "toast";
  }, 4000);
}

function showStatus(message, type = "info") {
  if (type === "success") {
    statusText.innerHTML = `<b style="color:#00ffcc;">✅ ${message}</b>`;
  } else if (type === "error") {
    statusText.innerHTML = `<b style="color:#ff5c5c;">❌ ${message}</b>`;
  } else {
    statusText.innerText = message;
  }
}

// Prevent Enter key submit
document.getElementById("authForm").addEventListener("submit", (e) => {
  e.preventDefault();
});

// ================================
// START CAMERA (stable)
// ================================
async function startCamera() {
  try {
    showStatus("Status: Waiting...");

    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: "user"
      },
      audio: false
    });

    video.srcObject = stream;

    await new Promise((resolve) => {
      video.onloadeddata = () => resolve();
    });

    await video.play();
    showStatus("Status: Waiting...");
  } catch (err) {
    console.error("Camera error:", err);
    showStatus("Camera access failed. Please allow permission.", "error");
    showToast("Camera permission required", "error");
  }
}
startCamera();

// ================================
// CAPTURE IMAGE
// ================================
function captureImage() {
  const ctx = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL("image/jpeg");
}

// ================================
// REGISTER
// ================================
async function registerUser() {
  try {
    showStatus("Registering...");

    if (!emailInput.value || !passwordInput.value) {
      showStatus("Please enter Email and Password!", "error");
      showToast("Please enter Email and Password", "error");
      return;
    }

    const res = await fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: emailInput.value,
        password: passwordInput.value,
        image: captureImage()
      })
    });

    const data = await res.json();

    if (res.ok) {
      showStatus(data.message || "User registered successfully", "success");
      showToast("User registered successfully ✅", "success");
    } else {
      showStatus(data.message || "Registration Failed", "error");
      showToast(data.message || "Registration Failed ❌", "error");
    }
  } catch (err) {
    console.error(err);
    showStatus("Register Error: " + err.message, "error");
    showToast("Server error ❌", "error");
  }
}

// ================================
// VERIFY
// ================================
async function verifyUser() {
  try {
    showStatus("Verifying...");

    if (!emailInput.value || !passwordInput.value) {
      showStatus("Please enter Email and Password!", "error");
      showToast("Please enter Email and Password", "error");
      return;
    }

    const res = await fetch("http://127.0.0.1:5000/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: emailInput.value,
        password: passwordInput.value,
        image: captureImage()
      })
    });

    const data = await res.json();

    if (res.ok) {
      let extra = "";
      if (data.distance !== undefined) extra = ` | Distance: ${data.distance}`;
      showStatus((data.message || "Face verified successfully") + extra, "success");
      showToast(data.message || "Face verified successfully ✅", "success");
    } else {
      showStatus(data.message || "Face verification failed", "error");
      showToast(data.message || "Face verification failed ❌", "error");
    }
  } catch (err) {
    console.error(err);
    showStatus("Verify Error: " + err.message, "error");
    showToast("Server error ❌", "error");
  }
}

// Buttons
registerBtn.addEventListener("click", registerUser);
verifyBtn.addEventListener("click", verifyUser);

