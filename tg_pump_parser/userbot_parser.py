from telethon import TelegramClient, events
import re
import os
import json
TOKENS_TRACK_FILE = 'forwarded_tokens_mex.json'

if os.path.exists(TOKENS_TRACK_FILE):
    with open(TOKENS_TRACK_FILE):
        token_counts = json.load(f)
else:
    token_counts = {}
api_id = 22056618
api_hash = "db2bf3b16f1788d38091014befe31c0d"
session_name = "user_session"

client = TelegramClient(session_name, api_id, api_hash)

SOURCE_CHANNEL = "dt_5p"
TARGET_CHAT_ID = -1002604238211
TARGET_THREAD_ID = 1745

SELECTED_TOKENS = [
    "DBR", "ELDE", "GEAR", "SHM", "EGL1", "GFM",
    "UPTOP", "AMB", "EDGEN", "MYX", "BID", "AURASOL", "IRISVIRTUAL", "TAG", "NEIROETH", "IDOL", "DARK"
]
SELECTED_TOKENS = [t.upper() for t in SELECTED_TOKENS]

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    text = event.raw_text
    print(f"Incoming: {text}")

    # FIX: виклик text.upper() був без дужок, треба text.upper()
    found_tokens = re.findall(r"\$([A-Z][A-Z0-9]{1,9})", text.upper())
    print(f"Found tokens: {found_tokens}")

    for token in found_tokens:
        token = token.upper()
        if token in SELECTED_TOKENS:
            print(f"✅ SELECTED: {token}")
            await client.send_message(
                entity=TARGET_CHAT_ID,
                message=event.message,
                reply_to=TARGET_THREAD_ID
            )
            break  # надсилаємо лише один раз на повідомлення

        counts = token_counts.get(token, 0)
        if counts <3:
            token_counts[token] = counts + 1
            await client.send_message(
                entity=TARGET_CHAT_ID,
                message=event.message,
                reply_to=TARGET_THREAD_ID
            )
            print(f"NEW {token}: {counts + 1}/3")
            with open(TOKENS_TRACK_FILE, "w") as f:
                json.dump(token_counts, f)
        else:
            print(f"❌ Skipped: {token}")

async def preload_token_counts():
    print("⏳ Loading previous 10000 messages from history...")
    messages = await client.get_messages(SOURCE_CHANNEL, limit=10000)
    added = 0
    for msg in messages:
        if msg.text:
            tokens = re.findall(r"\b[A-Z0-9]{2,10}\b", msg.text)
            for token in tokens:
                token = token.upper()
        if token not in SELECTED_TOKENS:
                    if token not in token_counts:
                        token_counts[token] = 1
                        added += 1
                    else:
                        token_counts[token] += 1
    print(f"✅ Preloaded {added} tokens from history")
    
async def main():
    await preload_token_counts()
    print("✅ MEXC userbot started")
    await client.run_until_disconnected()

client.start()
with client:
    client.loop.run_until_complete(main())
