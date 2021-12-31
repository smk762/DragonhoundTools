#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
import subprocess


SCRIPT_PATH = sys.path[0]
ACTIVATE_COMMANDS = requests.get("http://stats.kmd.io/api/atomicdex/activation_commands/").json()["commands"]


def colorize(string, color):
    colors = {
        'black':'\033[30m',
        'error':'\033[31m',
        'red':'\033[31m',
        'green':'\033[32m',
        'orange':'\033[33m',
        'blue':'\033[34m',
        'purple':'\033[35m',
        'cyan':'\033[36m',
        'lightgrey':'\033[37m',
        'table':'\033[37m',
        'darkgrey':'\033[90m',
        'lightred':'\033[91m',
        'lightgreen':'\033[92m',
        'yellow':'\033[93m',
        'lightblue':'\033[94m',
        'status':'\033[94m',
        'pink':'\033[95m',
        'lightcyan':'\033[96m',
    }
    if color not in colors:
        return str(string)
    else:
        return colors[color] + str(string) + '\033[0m'


def success_print(msg):
  print(colorize(msg, "green"))


def dark_print(msg):
  print(colorize(msg, "darkgrey"))


def status_print(msg):
  print(colorize(msg, "status"))


def error_print(msg):
  print(colorize(msg, "error"))


def mm2_proxy(params):
  params.update({"userpass": MM2_USERPASS})
  #print(json.dumps(params))
  r = requests.post(MM2_IP, json.dumps(params))
  return r.json()

def disable_coin(coin):
    return mm2_proxy({"method":"disable_coin","coin":coin})

def scan_electrums_for_balances(seed_phrase):

    ignore_coins = ["tBLK", "GIN", "LYNX", "PGT", "CIPHS", "VOTE2021", "HUSH3"]
    balance_found = False
    seed_phrases = {
        seed_phrase: {}
    }
    for protocol in ACTIVATE_COMMANDS:
        for coin in ACTIVATE_COMMANDS[protocol]:
            activation_command = ACTIVATE_COMMANDS[protocol][coin]
            
            try:
                resp = mm2_proxy(ACTIVATE_COMMANDS[protocol][coin])
                if "balance" in resp:
                    if float(resp["balance"]) > 0:
                        balance_found = True
                        seed_phrases[seed_phrase].update({
                            coin: {
                                "address":resp["address"],
                                "balance":resp["balance"],
                            }
                        })
                        success_print(f'{coin} | {resp["address"]} | {resp["balance"]}')
                    else:
                        dark_print(f'{coin} | {resp["address"]} | {resp["balance"]}')
                        disable_coin(coin)
                else:
                    dark_print(f'{coin}: {resp}')
                    disable_coin(coin)
                time.sleep(0.01)

            except Exception as e:
                dark_print("---------------------------")
                dark_print(f"{coin}: {e}")
                dark_print("---------------------------")

    if balance_found:
        with open('seed_phrases.json', 'w', encoding='utf-8') as f:
            json.dump(seed_phrases, f, ensure_ascii=False, indent=4)
        status_print(f"Found balances listed in seed_phrases.json")
    else:
        status_print(f"No balances found for seed")


if __name__ == '__main__':

    if os.path.exists(f"{SCRIPT_PATH}/MM2.json"):
        with open(f"{SCRIPT_PATH}/MM2.json", "r") as f:
            MM2_JSON = json.load(f)
            if "passphrase" in MM2_JSON:
                mm2_seed_phrase = MM2_JSON["passphrase"]
    else:
        error_print("No MM2.json found, exiting...")
        sys.exit()

    MM2_USERPASS = MM2_JSON["rpc_password"]

    mm2_ip = "http://127.0.0.1"
    mm2_port = 7783

    if "rpcip" in MM2_JSON:
        mm2_ip = MM2_JSON["rpcip"]

    if "rpcport" in MM2_JSON:
        mm2_port = MM2_JSON["rpcport"]

    MM2_IP = f"{mm2_ip}:{mm2_port}"

    time.sleep(5)
    scan_electrums_for_balances(mm2_seed_phrase)
    time.sleep(5)