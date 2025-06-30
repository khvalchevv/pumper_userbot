from telethon import TelegramClient, events
import re
import json
import os

api_id = 22056618
api_hash = "db2bf3b16f1788d38091014befe31c0d"
session_name = "user_session_gate"

client = TelegramClient(session_name, api_id, api_hash)

SOURCE_CHANNEL_2 = "gate_5p"
TARGET_CHAT_ID_2 = -1002604238211
TARGET_THREAD_ID_2 = 2899

SELECTED_TOKENS = ["PAWS", "IDOL", "ELDE", "SPK", "EDGEN", "PRAI", "WLD", "BLUE",
    "WHY", "ORDER", "FLY", "KEY", "LUCE", "ZCX", "KILO", "BID", "SHM", "BLZ", "OMG",
    "AMB", "IMT", "PFWS"
]

TOKENS_TRACK_FILE = "forwarded_tokens_gate.json"

if os.path.exists(TOKENS_TRACK_FILE):
    with open(TOKENS_TRACK_FILE, "r") as f:
        token_counts = json.load(f)
else:
    token_counts = {}

async def preload_token_counts():
    print("⏳ Loading previous 10000 messages from history...")
    messages = await client.get_messages(SOURCE_CHANNEL_2, limit=10000)
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

@client.on(events.NewMessage(chats=SOURCE_CHANNEL_2))
async def handler(event):
    text = event.raw_text
    found = re.findall(r"\b[A-Z0-9]{2,10}\b", text)
    tokens_in_msg = [t for t in found if t.isupper()]

    for token in tokens_in_msg:
        if token in SELECTED_TOKENS:
            await client.send_message(
                entity=TARGET_CHAT_ID_2,
                message=event.message,
                reply_to=TARGET_THREAD_ID_2
            )
            print(f"✅ SELECTED: {token}")
            return

        count = token_counts.get(token, 0)
        if count < 3:
            token_counts[token] = count + 1
            await client.send_message(
                entity=TARGET_CHAT_ID_2,
                message=event.message,
                reply_to=TARGET_THREAD_ID_2
            )
            print(f"🆕 NEW {token}: {count + 1}/3")
            with open(TOKENS_TRACK_FILE, "w") as f:
                json.dump(token_counts, f)
            return

async def main():
    await preload_token_counts()
    print("✅ Second userbot started")
    await client.run_until_disconnected()

client.start()
with client:
    client.loop.run_until_complete(main())
