#!/usr/bin/env python3
import os
import time
import base58
import bitcoin
from bitcoin.core import x
from bitcoin.core import CoreMainParams
from bitcoin.wallet import P2PKHBitcoinAddress
from logger import logger

BASE58_PARAMS = {
    "LTC": {'pubtype': 48, 'wiftype': 5, 'p2shtype': 176},
    "AYA": {"pubtype": 23, "wiftype": 176, "p2shtype": 5},
    "EMC2": {"pubtype": 33, "wiftype": 176, "p2shtype": 5},
    "KMD": {"pubtype": 60, "wiftype": 188, "p2shtype": 85},
    "MIL": {"pubtype": 50, "wiftype": 239, "p2shtype": 196}
}

def get_CoinParams(coin):
    params = BASE58_PARAMS[coin]
    class CoinParams(CoreMainParams):
        MESSAGE_START = b'\x24\xe9\x27\x64'
        DEFAULT_PORT = 7770
        BASE58_PREFIXES = {
            'PUBKEY_ADDR': params["pubtype"],
            'SCRIPT_ADDR': params["p2shtype"],
            'SECRET_KEY': params["wiftype"]
        }
    return CoinParams


coin_params = {}
for coin in BASE58_PARAMS:
    coin_params[coin] = get_CoinParams(coin)


def get_addr_from_pubkey(pubkey: str, coin: str="KMD") -> str:
    if coin not in coin_params:
        coin = "KMD"
    bitcoin.params = coin_params[coin]
    try:
        return str(P2PKHBitcoinAddress.from_pubkey(x(pubkey)))
    except Exception as e:
        os.system('clear')
        print(f"\n\n")
        logger.error(f"Error! {e}")
        print(f"\n\n")
        time.sleep(1)
        return ""
