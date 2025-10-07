from flask import Flask, request, render_template, session, redirect, url_for
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
    session_str = None
    code_sent = False

    if request.method == "POST":
        # Step 1: Sending code
        if "api_id" in request.form:
            session["api_id"] = int(request.form["api_id"])
            session["api_hash"] = request.form["api_hash"]
            session["phone"] = request.form["phone"]
            session["password"] = request.form.get("password")
            api_id = session["api_id"]
            api_hash = session["api_hash"]
            phone = session["phone"]

            async def send_code():
                async with TelegramClient(StringSession(), api_id, api_hash) as client:
                    await client.send_code_request(phone)

            asyncio.run(send_code())
            code_sent = True

        # Step 2: User enters code
        elif "code" in request.form:
            code = request.form["code"]
            api_id = session.get("api_id")
            api_hash = session.get("api_hash")
            phone = session.get("phone")
            password = session.get("password")

            async def generate_session():
                async with TelegramClient(StringSession(), api_id, api_hash) as client:
                    await client.sign_in(phone=phone, code=code, password=password)
                    return client.session.save()

            session_str = asyncio.run(generate_session())

    return render_template("index.html", session_str=session_str, code_sent=code_sent)

if __name__ == "__main__":
    app.run(debug=True)
