#!/usr/bin/env python3
import os
import datetime
import logging
import requests
from os.path import expanduser
from dotenv import load_dotenv
from logging import Handler, Formatter


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
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

class RequestsHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data=payload).content

class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()

    def format(self, record):
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        return f"<i>{t}</i><pre>\n{record.msg}</pre>"

logger = logging.getLogger("tg_alert")
logger.setLevel(logging.WARNING)
handler = RequestsHandler()
formatter = LogstashFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_telegram(msg):
    logger.warning(msg)

