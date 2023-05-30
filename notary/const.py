#!/usr/bin/env python3
import os
from os.path import expanduser
from dotenv import load_dotenv

# DEPS:
# sudo apt-get install libgnutls28-dev python3 python3-pip python3-setuptools python3-six
# pip3 install -r requirements.txt
# Then setup .env file with required variables
# See https://sean-bradley.medium.com/get-telegram-chat-id-80b575520659 to get TELEGRAM_CHAT_ID
# See https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token to get TELEGRAM_TOKEN

load_dotenv()
HOME = expanduser("~")
NODE = os.getenv('NODE') # Main or 3P
SEASON = os.getenv('SEASON') # Integer, e.g. 7
NN_ADDR = os.getenv('NN_ADDR') # KMD address of your node
PUBKEY = os.getenv('NN_PUBKEY') # Pubkey of your node
SWEEP_ADDR = os.getenv('SWEEP_ADDR') # KMD address to sweep mined funds to
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') # Telegram bot token
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') # Telegram chat ID
NN_PRIVKEY = os.getenv("NN_PRIVKEY") # KMD Privkey of your node