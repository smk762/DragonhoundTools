#!/usr/bin/env python3
import os
import json
import time
import random
import logging
import telebot
import datetime
import threading
import concurrent.futures
from telebot import util
from telegram import ParseMode
import requests
from datetime import datetime as dt
from random import shuffle

import lib_electrum_v2
from dotenv import load_dotenv
from logging import Handler, Formatter

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
BB_PK = os.getenv("BB_PK")
BB_ADDR = os.getenv("BB_ADDR")
SEASON = "Season_6"
FUNDS_DISTRIBUTOR = "dragonhound_DEV"
FUNDS_DISTRIBUTOR_ADDR = "RDragoNHdwovvsDLSLMiAEzEArAD3kq6FN"

ELECTRUMS = requests.get("http://stats.kmd.io/api/info/electrums/").json()["results"]
EXPLORERS = requests.get("http://stats.kmd.io/api/info/explorers/").json()["results"]
NOTARY_ADDRESSES = requests.get(f"http://stats.kmd.io/api/wallet/notary_addresses/").json()

if 'TOKEL' not in ELECTRUMS:
    ELECTRUMS.update({"TOKEL":["1.eu.tokel.electrum.dexstats.info:10077"]})

EXCLUDED_MAIN_CHAINS = ["BTC", "RFOX", "PGT", "VOTE2021", "AXO", "BTCH", "OOT", "WLC21", "COQUICASH"]
EXCLUDED_3P_CHAINS = ["LTC", "HUSH3", "PBC", "GLEEC_3P", "BTC", "SFUSD"]
EXCLUDED_NOTARIES = []

balance_thresholds = {
    "LTC": 0.11,
    "AYA": 1.2,
    "EMC2": 1.2,
    "GLEEC_3P": 1.2,
    "OTHER": 0.25,
    "KMD": 0.01
}

special_balance_thresholds = {
    "LTC": 0.11,
    "AYA": 1.2,
    "EMC2": 1.2,
    "GLEEC_3P": 1.2,
    "MIL": 1.2,
    "OTHER": 0.5,
    "KMD": 0.01
}


balance_replenish = {
    "LTC": 0.2,
    "AYA": 3,
    "EMC2": 3,
    "MIL": 3,
    "GLEEC_3P": 2,
    "OTHER": 0.5,
}

balances_dict = {}
chains_dict = {}
notaries = []

now = int(time.time())
human_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
time.ctime(now)

class RequestsHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN),
                             data=payload).content


class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()

    def format(self, record):
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)


class electrum_thread(threading.Thread):
    def __init__(self, chain, addr, pubkey, notary, season, server):
        threading.Thread.__init__(self)
        self.pubkey = pubkey
        self.chain = chain
        self.addr = addr
        self.notary = notary
        self.season = season
        self.server = server
    def run(self):
        thread_electrum(self.chain, self.addr, self.pubkey,
                        self.notary, self.season, self.server)


def thread_electrum(chain, addr, pubkey, notary, season, server):

    if season not in balances_dict:
        balances_dict.update({season:{}})

    if server not in balances_dict[season]:
        balances_dict[season].update({server:{}})

    if chain not in balances_dict[season][server]:
        balances_dict[season][server].update({chain:{}})

    if notary not in balances_dict[season][server][chain]:
        balances_dict[season][server][chain].update({notary:{}})

    try:
        url, port = random.choice(ELECTRUMS[chain]).split(":")
    except:
        url = None
        port = None

    balance_data = lib_electrum_v2.get_balance(chain, addr, pubkey, url, port, notary)

    balances_dict[season][server][chain][notary].update({
                                    "address":addr,
                                    "balance":balance_data[0],
                                    "source":balance_data[1]
                                })

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
handler = RequestsHandler()
formatter = LogstashFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

def scan_balances():

    global balances_dict
    global chains_dict
    global notaries

    for server in NOTARY_ADDRESSES[SEASON]:

        if server not in chains_dict:
            chains_dict.update({server:[]})

        notaries = list(NOTARY_ADDRESSES[SEASON][server].keys())
        shuffle(notaries)
        for notary in notaries:
            thread_list = []

            if notary not in notaries:
                notaries.append(notary)

            pubkey = NOTARY_ADDRESSES[SEASON][server][notary]["pubkey"]
            chains = list(NOTARY_ADDRESSES[SEASON][server][notary]["addresses"].keys())
            shuffle(chains)
            for chain in chains:
                if (server == "Main" and chain not in EXCLUDED_MAIN_CHAINS) or (server == "Third_Party" and chain not in EXCLUDED_3P_CHAINS):
                    if chain not in chains_dict[server]:
                        chains_dict[server].append(chain)

                    address = NOTARY_ADDRESSES[SEASON][server][notary]["addresses"][chain]

                    if chain == "GLEEC" and server == "Third_Party":
                        chain = "GLEEC-OLD"

                    thread_list.append(electrum_thread(chain, address, pubkey, notary, SEASON, server))

            for thread in thread_list:
                thread.start()
                time.sleep(0.1)
            time.sleep(5)

        chains_dict[server].sort()
    notaries.sort()

def gen_ARRR_string(z_sendmany):
    ARRR_addresses = []
    send_str = ""
    amount = balance_replenish["OTHER"]
    for i in z_sendmany:
        print(i)
        ARRR_addresses.append(i["address"])
    addr_Array = " ".join(ARRR_addresses)
    send_str = f'ARR_addr=({addr_Array}); amount={amount}; '
    send_str += 'for addr in "${ARR_addr[@]}"; do komodo-cli -ac_name=PIRATE sendtoaddress $addr $amount; done;'
    return send_str

scan_balances()
i = 0
while True:
    i += 1
    finished = True

    for server in balances_dict[SEASON]:
        for chain in chains_dict[server]:
            if chain == "GLEEC" and server == "Third_Party":
                chain = "GLEEC-OLD"
            if chain not in balances_dict[SEASON][server]:
                print(f"Waiting for {server} {chain} response...")
                finished = False
            else:
                if len(balances_dict[SEASON][server][chain]) != len(notaries):
                    print(f"Waiting for balances_dict[{SEASON}][{server}][{chain}] notaries to populate... {len(balances_dict[SEASON][server][chain])}/{len(notaries)} complete....")
                    finished = False

    if finished:
        print(f"balances_dict fully populated, continuing...")
        break

    if i > 30:
        print(f"balances_dict not populated after 5 minutes, continuing anyway...")
        break

    time.sleep(10)


chain_fails = {}
low_balances_by_notary = {}
low_balances_by_chain = {}
sources = {}

for server in balances_dict[SEASON]:
    for chain in chains_dict[server]:
        if (server == "Main" and chain not in EXCLUDED_MAIN_CHAINS) or (server == "Third_Party" and chain not in EXCLUDED_3P_CHAINS):
            if chain == "GLEEC" and server == "Third_Party":
                chain = "GLEEC-OLD"
            if chain in balance_thresholds:
                threshold = balance_thresholds[chain]
            else:
                threshold = balance_thresholds["OTHER"]

            for notary in notaries:
                if notary not in EXCLUDED_NOTARIES:
                    data = balances_dict[SEASON][server][chain][notary]
                    if "balance" in data:
                        balance = data["balance"]
                    else:
                        print(data)
                        balance = -1

                    if balance == -1:
                        if chain not in chain_fails:
                            chain_fails.update({chain:[]})
                        chain_fails[chain].append(notary)
                        source = "NO SRC"

                    else:
                        address = data["address"]
                        source = data["source"]
                        if float(balance) <= threshold or notary == FUNDS_DISTRIBUTOR:

                            if notary not in low_balances_by_notary:
                                low_balances_by_notary.update({notary:{}})
                            low_balances_by_notary[notary].update({
                                    chain:{
                                        "balance":balance,
                                        "address":address
                                    }
                                })

                            if chain not in low_balances_by_chain:
                                low_balances_by_chain.update({chain:{}})
                            low_balances_by_chain[chain].update({
                                    notary:{
                                        "balance":balance,
                                        "address":address
                                    }
                                })

                    if source not in sources:
                        sources.update({source:[]})

                    if chain not in sources[source]:
                        sources[source].append(chain)



# GENERATE SUMMARY TABLE
msg = "*"*74+"\n"
msg += "|"+'{:^70}'.format(SEASON.replace('_', ' ').upper()+" NOTARY BALANCES REPORT: "+str(human_now))+"|\n"

for chain in low_balances_by_chain:
    msg += "*"*24+'{:^26}'.format(chain.upper())+"*"*24+"\n"
    notaries = list(low_balances_by_chain[chain].keys())
    notaries.sort()
    for notary in notaries:
        if notary != FUNDS_DISTRIBUTOR:
            address = low_balances_by_chain[chain][notary]["address"]
            balance = low_balances_by_chain[chain][notary]["balance"]
            msg += "|"+'{:^70}'.format('{:^18}'.format(notary)+"|"+'{:^36}'.format(address)+" | "+'{:^10}'.format(str(balance)))+"|\n"
            if len(msg) > 2500:
                print(len(msg))
                logger.warning(msg)
                msg = ''

msg += "*"*74+"\n"

for chain in chain_fails:
    msg += "|"+'{:^70}'.format('{:^18}'.format('')+"|"+'{:^36}'.format(str(len(chain_fails[chain]))+" failed queries for "+chain).upper()+" | "+'{:^10}'.format(''))+"|\n"
    if len(msg) > 2500:
        print(msg)
        logger.warning(msg)
        msg = ''



# EXPORT DATA TO JSON
balance_data = {
    "low_balances_by_notary":low_balances_by_notary,
    "low_balances_by_chain":low_balances_by_chain,
    "chain_fails":chain_fails,
    "time":int(time.time()),
    "sources": sources
}

with open(os.path.dirname(os.path.abspath(__file__))+'/balances_report.json', 'w+') as j:
    json.dump(balance_data, j, indent = 4, sort_keys=True)


# GENERATE SUMMARY TABLE
for chain in low_balances_by_chain:
    if len(low_balances_by_chain[chain]) > 3:

        sendmany = {}
        z_sendmany = []


        if chain in balance_replenish:
            val = balance_replenish[chain]
        else:
            val = balance_replenish["OTHER"]

        for notary in low_balances_by_notary:
            if chain in low_balances_by_notary[notary] and notary not in EXCLUDED_NOTARIES:
                if chain != 'PIRATE':
                    sendmany.update({low_balances_by_notary[notary][chain]["address"]:val})
                elif low_balances_by_notary[notary][chain]["address"] != FUNDS_DISTRIBUTOR_ADDR:
                    z_sendmany.append({"address":low_balances_by_notary[notary][chain]["address"], "amount":val})
        try:

            if chain != 'PIRATE':
                if chain == "AYA":
                    msg += 'aryacoin-cli sendmany "" "'+json.dumps(sendmany).replace('"', '\\"')+'"\n'
                elif chain == "CHIPS":
                    msg += 'chips-cli sendmany "" "'+json.dumps(sendmany).replace('"', '\\"')+'"\n'
                elif chain == "LTC":
                    msg += 'litecoin-cli sendmany "" "'+json.dumps(sendmany).replace('"', '\\"')+'"\n'
                elif chain == "EMC2":
                    msg += 'emc-cli sendmany "" "'+json.dumps(sendmany).replace('"', '\\"')+'"\n'
                else:
                    msg += "komodo-cli -ac_name="+chain+' sendmany "" "'+json.dumps(sendmany).replace('"', '\\"')+'"\n'

            else:
                logger.warning(gen_ARRR_string(z_sendmany)+"\n")

            if len(msg) > 2500:
                print(msg)
                logger.warning(msg)
                msg = ''
        except Exception as e:
            print(f"{chain} failed in low_balance_chains loop: {e}")

if msg != '':
    print(msg)
    logger.warning(msg)


print(z_sendmany)
print(gen_ARRR_string(z_sendmany))
