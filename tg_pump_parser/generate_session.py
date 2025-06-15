from telethon.sync import TelegramClient

api_id = 22929642
api_hash = "9e1cb2954a8822c811fa4f0e78a9ffe4"
session_name = "user_session"  # буде збережено як user_session.session

with TelegramClient(session_name, api_id, api_hash) as client:
    print("✅ Сесія збережена!")
