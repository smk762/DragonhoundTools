#!/usr/bin/env python3
import os
import time
import json
import const
import requests
from logger import logger


def chunkify(data: list, chunk_size: int):
    return [data[x:x+chunk_size] for x in range(0, len(data), chunk_size)]



def refresh_external_data(file, url):
    if not os.path.exists(file):
        data = requests.get(url).json()
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    else:
        now = int(time.time())
        mtime = os.path.getmtime(file)
        if now - mtime > 21600: # 6 hours
            data = requests.get(url).json()
            with open(file, "w") as f:
                json.dump(data, f, indent=4)
    with open(file, "r") as f:
        return json.load(f)


def get_coins_config():
    return refresh_external_data(const.COINS_CONFIG_PATH, const.COINS_CONFIG_URL)


def get_seednode_versions():
    return refresh_external_data(const.SEEDNODE_VERSIONS_PATH, const.SEEDNODE_VERSIONS_URL)


def get_vouts(coin: str, address: str, value: float, tx_size: int) -> dict:
    fee = get_fee(coin, tx_size)
    print(f"{coin} fee: {fee}")
    return {address: value - fee}


def get_fee(coin: str, tx_size) -> float:
    if coin in ["LTC"]:
        fee = tx_size * 0.00000002
    elif coin in ["EMC", "CHIPS", "AYA"]:
        if coin in const.LARGE_UTXO_COINS:
            fee = 0.00010000
        else:
            fee = 0.00001000


def get_inputs(utxos: list, exclude_utxos: list) -> list:
    value = 0
    inputs = []
    for utxo in utxos:
        try:
            if {"txid": utxo["txid"], "vout": utxo["vout"]} not in exclude_utxos:
                inputs.append({"txid": utxo["txid"], "vout": utxo["vout"]})
                if "satoshis" in utxo:
                    value += utxo["satoshis"]
                elif "amount" in utxo:
                    value += utxo["amount"] * 100000000
            else:
                logger.debug(f"excluding {utxo['txid']}:{utxo['vout']}")
        except Exception as e:
            logger.debug(e)
            logger.debug(utxo)
    value = round(value/100000000, 8)
    return [inputs, value]
