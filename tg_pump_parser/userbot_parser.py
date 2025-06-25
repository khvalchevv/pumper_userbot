from telethon import TelegramClient, events
import re
import os
import json

api_id = 22056618
api_hash = "db2bf3b16f1788d38091014befe31c0d"
session_name = "user_session"

client = TelegramClient(session_name, api_id, api_hash)

SOURCE_CHANNEL = "dt_5p"
TARGET_CHAT_ID = -1002604238211
TARGET_THREAD_ID = 1745

SELECTED_TOKENS = ["DBR", "ELDE", "GEAR", "WHITE", "SHM", "EGL1", "GFM", "LMWR", "AMB", "EDGEN", "GHIBLI", "BID", "AURASOL"]
TOKENS_TRACK_FILE = "forwarded_tokens_mexc.json"

# Завантажити лічильники токенів
if os.path.exists(TOKENS_TRACK_FILE):
    with open(TOKENS_TRACK_FILE, "r") as f:
        token_counts = json.load(f)
else:
    token_counts = {}

# 🔄 Попередній аналіз історії (1000 повідомлень)
async def preload_token_counts():
    async for msg in client.iter_messages(SOURCE_CHANNEL, limit=1000):
        if msg.text:
            tokens = re.findall(r"\b[A-Z0-9]{2,10}\b", msg.text)
            for token in tokens:
                token = token.upper()
                if token not in SELECTED_TOKENS:
                    token_counts[token] = token_counts.get(token, 0) + 1

# 🔁 Обробка нових повідомлень
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    text = event.raw_text
    found = re.findall(r"\b[A-Z0-9]{2,10}\b", text)
    tokens_msg = [t for t in found if t.isupper()]

    for token in tokens_msg:
        if token in SELECTED_TOKENS:
            await client.send_message(
                entity=TARGET_CHAT_ID,
                message=event.message,
                reply_to=TARGET_THREAD_ID
            )
            print(f"✅ SELECTED: {token}")
            return
        else:
            count = token_counts.get(token, 0)
            if count < 3:
                await client.send_message(
                    entity=TARGET_CHAT_ID,
                    message=event.message,
                    reply_to=TARGET_THREAD_ID
                )
                token_counts[token] = count + 1
                print(f"➕ NEW: {token} ({count + 1}/3)")

                with open(TOKENS_TRACK_FILE, "w") as f:
                    json.dump(token_counts, f)
                return

print("✅ First userbot (MEXC) started")
client.start()
client.loop.run_until_complete(preload_token_counts())
client.run_until_disconnected()
