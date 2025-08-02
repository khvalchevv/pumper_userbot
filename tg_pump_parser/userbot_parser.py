from telethon import TelegramClient, events
import re


api_id = 22056618
api_hash = "db2bf3b16f1788d38091014befe31c0d"
session_name = "user_session"

client = TelegramClient(session_name, api_id, api_hash)

SOURCE_CHANNEL = "dt_5p"
TARGET_CHAT_ID = -1002604238211
TARGET_THREAD_ID =1745

SELECTED_TOKENS = ["IDOL", "ORDER", "FLY", "BLZ", "OMG", "BROCCOLI", "DBR", "EDGE", "EGL1", "NEIROETH", "GFM", "TAG", "NEIROETH", "BLUM"]


@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    text = event.raw_text
    found_tokens = re.findall(r"\$([A-Z0-9]{2,10})", text.upper())
    print(f"Incoming message: {text}")
    print(f"Found tokens: {found_tokens}")

    for token in found_tokens:
        if token in SELECTED_TOKENS:
            await client.send_message(
                entity=TARGET_CHAT_ID,
                message=event.message,
                reply_to=TARGET_THREAD_ID
            )
            print(f"✅ SELECTED: {token}")
            return
        else:
            print(f"Skipped: {token}")

async def main():
    print("✅ First userbot started")
    await client.run_until_disconnected()

client.start()
with client:
    client.loop.run_until_complete(main())
