from telethon import TelegramClient, events
import re

api_id = 22056618
api_hash = "db2bf3b16f1788d38091014befe31c0d"
session_name = "user_session"

client = TelegramClient(session_name, api_id, api_hash)

SOURCE_CHANNEL = "dt_5p"
TARGET_CHAT_ID = -1002604238211
TARGET_THREAD_ID = 1745

SELECTED_TOKENS = [
    "DBR", "ELDE", "GEAR", "SHM", "EGL1", "GFM",
    "UPTOP", "AMB", "EDGEN", "MYX", "BID", "AURASOL", "IRISVIRTUAL", "TAG", "NEIROETH", "IDOL",
]

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    text = event.raw_text
    found_tokens = re.findall(r"\b[A-Z0-9]{2,10}\b", text)

    for token in found_tokens:
        if token.upper() in SELECTED_TOKENS:
            await client.send_message(
                entity=TARGET_CHAT_ID,
                message=event.message,
                reply_to=TARGET_THREAD_ID
            )
            print(f"✅ SELECTED: {token}")
            break  # надсилаємо лише один раз на повідомлення

print("✅ MEXC userbot started")
client.start()
client.run_until_disconnected()
