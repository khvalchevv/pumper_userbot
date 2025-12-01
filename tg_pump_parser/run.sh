#!/bin/bash
cd /root/pumper_userbot/tg_pump_parser
source venv/bin/activate
nohup python userbot_parser.py > bot.log 2>&1 &
