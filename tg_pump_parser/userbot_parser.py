import re
import asyncio
import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from colorama import Fore, Style, init

# ----------------------------
# Ініціалізація кольорових логів
# ----------------------------
init(autoreset=True)

# ----------------------------
# Завантаження змінних середовища
# ----------------------------
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "user_session")

SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
TARGET_THREAD_ID = int(os.getenv("TARGET_THREAD_ID", "0"))

SELECTED_TOKENS = ["COINBASE", "FIGSTOCK", "BABASTOCK", "ASMLSTOCK", "LLYSTOCK", "UNHSTOCK", "FUTUSTOCK", "CSCOSTOCK", "QQQSTOCK", "VSTOCK", "MUSTOCK", "FIGSTOCK", "PLTRSTOCK", "CRCLSTOCK", "GOOGLSTOCK", "AAPLSTOCK", "NVDASTOCK", "TSLASTOCK", "COINSTOCK", "QCOMSTOCK", "APPSTOCK", "BABASTOCK", "ADBESTOCK", "AMDSTOCK", "ORCLSTOCK", "MSTRSTOCK", "NFLXSTOCK", "MSFTSTOCK", "AVGOSTOCK", "MCDSTOCK", "METASTOCK", "AMZNSTOCK", "HOODSTOCK"]

SECOND_SOURCE_CHANNEL = os.getenv("SECOND_SOURCE_CHANNEL")
SECOND_TARGET_THREAD_ID = int(os.getenv("SECOND_TARGET_THREAD_ID", "0"))

SECOND_TOKENS = ["ORCLX", "HOODX", "DFDVX", "CRCLX", "QQQX", "PLTRX", "GOOGLX", "AAPLX", "NVDAX", "TSLAX", "COINX", "MSTRX", "METAX"]  # або твої

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ----------------------------
# Keepalive: щоб Telethon не “засинав”
# ----------------------------
async def keep_alive():
    while True:
        try:
            await client.get_dialogs()
            print(Fore.CYAN + "💤 Keepalive ping sent.")
        except Exception as e:
            print(Fore.RED + f"⚠️ Keepalive error: {e}")
        await asyncio.sleep(300)  # кожні 5 хвилин

# ----------------------------
# Основний хендлер нових повідомлень
# ----------------------------
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        text = event.raw_text or ""
        # шукати тільки справжні токени з $
        found_tokens = re.findall(r"\$([A-Z0-9]{2,10})", text)

        if not found_tokens:
            return

        print(Fore.BLUE + f"\n📩 Incoming message:")
        print(Style.BRIGHT + text)
        print(Fore.CYAN + f"🔍 Found tokens: {found_tokens}")

        target = await client.get_entity(TARGET_CHAT_ID)

        for token in found_tokens:
            token_upper = token.upper()
            if token_upper in SELECTED_TOKENS:
                await client.send_message(
                    entity=target,
                    message=f"{event.message.message}",
                    reply_to=TARGET_THREAD_ID if TARGET_THREAD_ID > 0 else None
                )
                print(Fore.GREEN + f"✅ Sent token: {token_upper}")
            else:
                print(Fore.YELLOW + f"⏭ Skipped token: {token_upper}")

    except Exception as e:
        print(Fore.RED + f"⚠️ Error while handling message: {e}")
@client.on(events.NewMessage(chats=SECOND_SOURCE_CHANNEL))
async def handler_second(event):
    try:
        text = event.raw_text or ""
        found_tokens = re.findall(r"\$([A-Z0-9]{2,10})", text)

        if not found_tokens:
            return

        print(Fore.BLUE + f"\n📩 Incoming message SECOND:")
        print(Style.BRIGHT + text)
        print(Fore.CYAN + f"🔍 Found tokens: {found_tokens}")

        target = await client.get_entity(TARGET_CHAT_ID)

        for token in found_tokens:
            token_upper = token.upper()
            if token_upper in SECOND_TOKENS:
                await client.send_message(
                    entity=target,
                    message=f"{event.message.message}",
                    reply_to=SECOND_TARGET_THREAD_ID if SECOND_TARGET_THREAD_ID > 0 else None
                )
                print(Fore.GREEN + f"✅ SECOND sent: {token_upper}")
            else:
                print(Fore.YELLOW + f"⏭ SECOND skipped: {token_upper}")

    except Exception as e:
        print(Fore.RED + f"⚠️ Error in SECOND handler: {e}")

# ----------------------------
# Основна функція запуску
# ----------------------------
async def main():
    print(Fore.MAGENTA + "🚀 Userbot started and listening...")
    client.loop.create_task(keep_alive())
    await client.run_until_disconnected()

# ----------------------------
# Точка входу
# ----------------------------
if __name__ == "__main__":
    client.start()
    with client:
        client.loop.run_until_complete(main())


