from flask import Flask
import threading
from telethon import TelegramClient, events
import asyncio
import os

api_id = 22056618
api_hash = "db2bf3b16f1788d38091014befe31c0d"

session_name = "user_session"  # ім'я сесії .session-файлу

SOURCE_CHANNEL = "dt_5p"  # Канал з якого парсиш
TARGET_CHAT_ID = -1002604238211
TARGET_THREAD_ID = 1745
TOKENS = ["$dbr", "$elde", "$gear", "$tibbir", "$white", "$shm", "$EGL1", "$GFM", "$IRISVIRTUAL"]

# Ініціалізація клієнта
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
        print(f"✅ Forwarded: {event.raw_text}")
    else:
        print(f"⛔ Skipped: {event.raw_text}")

async def main():
    me = await client.get_me()
    print(f"🤖 Logged in as: {me.username}")

app = Flask(__name__)

@app.route('/')
def home():
    return "Userbot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

client.start()
client.loop.run_until_complete(main())
client.run_until_disconnected()
