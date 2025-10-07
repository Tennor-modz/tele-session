from flask import Flask, request, jsonify, render_template, session
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))  # use env SECRET_KEY

@app.route("/")
def index():
    return render_template("index.html", message=os.environ.get("MESSAGE", ""))

@app.route("/send_code", methods=["POST"])
def send_code():
    data = request.json
    api_id = int(data["api_id"])
    api_hash = data["api_hash"]
    phone = data["phone"]
    password = data.get("password")

    # store in session
    session["api_id"] = api_id
    session["api_hash"] = api_hash
    session["phone"] = phone
    session["password"] = password

    async def _send_code():
        async with TelegramClient(StringSession(), api_id, api_hash) as client:
            await client.send_code_request(phone)

    asyncio.run(_send_code())
    return jsonify({"status": "ok", "message": "Code sent! Check your Telegram."})

@app.route("/generate_session", methods=["POST"])
def generate_session():
    data = request.json
    code = data["code"]
    api_id = session.get("api_id")
    api_hash = session.get("api_hash")
    phone = session.get("phone")
    password = session.get("password")

    async def _generate_session():
        async with TelegramClient(StringSession(), api_id, api_hash) as client:
            await client.sign_in(phone=phone, code=code, password=password)
            return client.session.save()

    session_str = asyncio.run(_generate_session())
    return jsonify({"status": "ok", "session_str": session_str})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
