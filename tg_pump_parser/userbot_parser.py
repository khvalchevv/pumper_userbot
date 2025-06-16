from flask import Flask
import threading
from telethon import TelegramClient, events
import asyncio

# Твої дані
api_id = 22965618
api_hash = "d2b073b1f61788d3809101abefe31c0d"
session_name = "user_session"

# Параметри
SOURCE_CHANNEL = "dt_5p"  # канал для парсингу
TARGET_CHAT_ID = -1002604238211
TARGET_THREAD_ID = 1745
TOKENS = ["$dbr", "$elde", "$gear", "$tibbir", "$white", "$shm", "$EGL1", "$GFM", "$IRISVIRTUAL", "$LMWR"]

# Ініціалізація Telethon
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    text = event.raw_text.lower()
    if any(token.lower() in text for token in TOKENS):
        await client.send_message(
            entity=TARGET_CHAT_ID,
            message=event.message,
            reply_to=TARGET_THREAD_ID
        )
        print(f"🟢 Forwarded: {event.raw_text}")
    else:
        print(f"🔴 Skipped: {event.raw_text}")

# Flask server для Railway
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Userbot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Старт
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

client.run_until_disconnected()
