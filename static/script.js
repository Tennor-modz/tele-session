const resultDiv = document.getElementById("result");

document.getElementById("send-code-btn").addEventListener("click", async () => {
    const api_id = document.getElementById("api_id").value.trim();
    const api_hash = document.getElementById("api_hash").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!api_id || !api_hash || !phone) {
        alert("Please fill all required fields!");
        return;
    }

    resultDiv.style.display = "block";
    resultDiv.innerText = "Sending code...";

    const res = await fetch("/send_code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_id, api_hash, phone, password })
    });

    const data = await res.json();
    if (data.status === "ok") {
        resultDiv.innerText = data.message;
        document.getElementById("form-step-1").style.display = "none";
        document.getElementById("form-step-2").style.display = "block";
    } else {
        resultDiv.innerText = "Failed to send code. Try again.";
    }
});

document.getElementById("generate-session-btn").addEventListener("click", async () => {
    const code = document.getElementById("code").value.trim();
    if (!code) { alert("Enter the code!"); return; }

    const res = await fetch("/generate_session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
    });
    const data = await res.json();
    if (data.status === "ok") {
        resultDiv.innerHTML = `<strong>Your session string:</strong><br>${data.session_str}`;
        document.getElementById("form-step-2").style.display = "none";
    }
});
