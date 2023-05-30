#!/usr/bin/env python3
import os
from os.path import expanduser
from dotenv import load_dotenv


# DEPS:
# sudo apt-get install libgnutls28-dev python3 python3-pip python3-setuptools python3-six
# pip3 install pyTelegramBotAPI==3.7.9
# pip3 install python-telegram-bot==12.7
# pip3 install slick-bitcoinrpc==0.1.4
# pip3 install python-dotenv==0.18.0
# Then setup .env file with required variables
# See https://sean-bradley.medium.com/get-telegram-chat-id-80b575520659 to get TELEGRAM_CHAT_ID
# See https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token to get TELEGRAM_TOKEN

load_dotenv()
HOME = expanduser("~")
NODE = os.getenv('NODE')
SEASON = os.getenv('SEASON')
SERVER = os.getenv('SERVER')
NN_ADDR = os.getenv('NN_ADDR')
PUBKEY = os.getenv('NN_PUBKEY')
SWEEP_ADDR = os.getenv('SWEEP_ADDR')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')