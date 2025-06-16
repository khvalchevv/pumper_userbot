from telethon.sync import TelegramClient

api_id = 22056618
api_hash = "db2bf3b16f1788d38091014befe31c0d"
session_name = "user_session"

with TelegramClient(session_name, api_id, api_hash) as client:
    print("✅ Сесія збережена!")
