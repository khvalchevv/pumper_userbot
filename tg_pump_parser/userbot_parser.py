from telethon import TelegramClient, events

api_id = 22965618
api_hash = "d2b073b1f61788d3809101abefe31c0d"
session_name = "user_session"
client = TelegramClient(session_name, api_id, api_hash)

TOKENS = ["DBR", "ELDE", "GEAR", "WHITE", "SHM", "EGL1", "GFM", "LMWR", "AMB", "EDGEN", "GHIBLI", "BID"]

SOURCE_CHANNEL = "dt_5p"
TARGET_CHAT_ID = -1002604238211
TARGET_THREAD_ID = 1745

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    if not event.message.message:
        return  # ігноруємо картинки, стікери тощо

    text = event.raw_text.upper()

    if any(token in text for token in TOKENS):
        await client.send_message(
            entity=TARGET_CHAT_ID,
            message=event.message,
            reply_to=TARGET_THREAD_ID
        )
        print(f"✅ Forwarded: {text[:100]}")
    else:
        print("⏭️ Skipped")

client.start()
print("🟢 Userbot started")
client.run_until_disconnected()
