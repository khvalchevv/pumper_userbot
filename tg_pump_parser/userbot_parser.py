from telethon import TelegramClient, events

# Твої дані
api_id = 22965618
api_hash = "d2b073b1f61788d3809101abefe31c0d"
session_name = "user_session"

# 🔧 Ініціалізація Telethon клієнта — ВАЖЛИВО щоб було ПЕРЕД @client.on!
client = TelegramClient(session_name, api_id, api_hash)

# Параметри
SOURCE_CHANNEL = "dt_5p"
TARGET_CHAT_ID = -1002604238211
TARGET_THREAD_ID = 1745

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    await client.send_message(
        entity=TARGET_CHAT_ID,
        message=event.message,
        reply_to=TARGET_THREAD_ID
    )
    print(f"🟢 Forwarded: {event.raw_text}")

client.start()
print("✅ Userbot started")
client.run_until_disconnected()