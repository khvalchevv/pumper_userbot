import re
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "user_session")

SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
TARGET_THREAD_ID = int(os.getenv("TARGET_THREAD_ID", "0"))

SELECTED_TOKENS = [
    "BEAT", "ORDER", "FLY", "BLZ", "OMG", "BROCCOLI", "DBR",
    "EDGE", "EGLI", "NEIROETH", "GFM", "TAG", "BLUM"
]

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ----------------------------
# Keepalive helper
# ----------------------------
async def keep_alive():
    while True:
        await client.get_dialogs()  # оновлює кеш діалогів
        await asyncio.sleep(300)  # кожні 5 хвилин

# ----------------------------
# Event handler
# ----------------------------
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        text = event.raw_text or ""
        found_tokens = re.findall(r"\b([A-Z0-9]{2,10})\b", text.upper())

        if not found_tokens:
            return

        print(f"📩 Incoming: {text}")
        print(f"🔍 Found tokens: {found_tokens}")

        target = await client.get_entity(TARGET_CHAT_ID)

        for token in found_tokens:
            if token in SELECTED_TOKENS:
                await client.send_message(
                    entity=target,
                    message=f"{event.message.message}",
                    reply_to=TARGET_THREAD_ID if TARGET_THREAD_ID > 0 else None
                )
                print(f"✅ Sent token: {token}")
            else:
                print(f"⏭ Skipped token: {token}")

    except Exception as e:
        print(f"⚠️ Error while handling message: {e}")

# ----------------------------
# Main entry
# ----------------------------
async def main():
    print("🚀 Userbot started and listening...")
    client.loop.create_task(keep_alive())
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.start()
    with client:
        client.loop.run_until_complete(main())

