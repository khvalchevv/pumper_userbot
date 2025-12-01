#!/bin/bash
echo "⛔️ Зупиняю старий процес..."
pkill -f userbot_parser.py
sleep 2

echo "⬇️ Оновлюю код з GitHub..."
git pull

echo "✅ Запускаю нового бота..."
source venv/bin/activate
nohup python userbot_parser.py > bot.log 2>&1 &

echo "🚀 Готово. Бот перезапущений."
