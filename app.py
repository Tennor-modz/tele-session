from flask import Flask, request, render_template_string, session, redirect, url_for
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for Flask session

HTML_FORM = """
<h2>Telegram Session Generator</h2>
<form method="POST">
API ID: <input name="api_id" required><br><br>
API Hash: <input name="api_hash" required><br><br>
Phone Number: <input name="phone" required><br><br>
2FA Password (optional): <input name="password"><br><br>
<button type="submit">Get Session String</button>
</form>
{% if session_str %}
<hr>
<p><b>Your Telegram session string:</b></p>
<p style="word-wrap: break-word;">{{ session_str }}</p>
{% endif %}
"""

# Step 1: Form submission
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["api_id"] = request.form["api_id"]
        session["api_hash"] = request.form["api_hash"]
        session["phone"] = request.form["phone"]
        session["password"] = request.form.get("password")
        return redirect(url_for("verify"))
    return render_template_string(HTML_FORM)

# Step 2: Ask for the code sent via Telegram
VERIFY_FORM = """
<h2>Enter the code sent to your Telegram</h2>
<form method="POST">
Code: <input name="code" required><br><br>
<button type="submit">Generate Session</button>
</form>
"""

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        code = request.form["code"]
        api_id = int(session.get("api_id"))
        api_hash = session.get("api_hash")
        phone = session.get("phone")
        password = session.get("password")

        async def generate_session():
            async with TelegramClient(StringSession(), api_id, api_hash) as client:
                await client.sign_in(phone=phone, code=code, password=password)
                return client.session.save()

        session_str = asyncio.run(generate_session())
        return render_template_string(HTML_FORM, session_str=session_str)
    return render_template_string(VERIFY_FORM)

if __name__ == "__main__":
    app.run(debug=True)
