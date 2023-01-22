#!/usr/bin/env python3
import os
import datetime
import logging
import requests
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

BTC_BALANCE_TG_TOKEN = os.getenv('BTC_BALANCE_TG_TOKEN')
BTC_ADRR = os.getenv('BTC_ADRR')
BTC_BALANCE_TG_CHAT_ID = os.getenv('BTC_BALANCE_TG_CHAT_ID')

class RequestsHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': BTC_BALANCE_TG_CHAT_ID,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        url = f"https://api.telegram.org/bot{BTC_BALANCE_TG_TOKEN}/sendMessage"
        r = requests.post(url,data=payload)
        return r.content

class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()

    def format(self, record):
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        r = "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)
        return r

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
handler = RequestsHandler()
formatter = LogstashFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

def send_telegram(msg):
    logger.warning(msg)

def get_btc_balance(addr):
    r = requests.get(f"https://api.blockcypher.com/v1/btc/main/addrs/{addr}/balance")
    return r.json()
    
if __name__ == '__main__':
    address_data = get_btc_balance(BTC_ADRR)
    if "error" in address_data:
        send_telegram(address_data["error"])
    else:
        try:
            with open('balance.txt', "r") as f:
                bal = float(f.read())
        except:
            bal = 0

        api_bal = address_data["balance"]/100000000
        if bal != api_bal:
            with open('balance.txt', "w") as f:
                print(f"Updating file with {api_bal} and sending alert...")
                f.write(str(api_bal))
            send_telegram(api_bal)
