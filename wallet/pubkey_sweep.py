#!/usr/bin/env python3
import time
import based_58
from const import INSIGHT_EXPLORERS
from logger import logger
from helper import chunkify, get_vouts, get_inputs
from insight_api import InsightAPI
from daemon import DaemonRPC

def get_utxos_from_api(coin: str, pubkey: str) -> list:
    address = based_58.get_addr_from_pubkey(pubkey, coin)
    if coin in INSIGHT_EXPLORERS:
        baseurl = INSIGHT_EXPLORERS[coin]
        if baseurl == "https://chips.explorer.dexstats.info/":
            insight = InsightAPI(baseurl, "api")
        else:
            insight = InsightAPI(baseurl)
        return insight.address_utxos(address)

def sweep(coin: str, pubkey: str, address: str) -> None:
    print()
    utxos = get_utxos_from_api(coin, pubkey)
    if len(utxos) == 0:
        logger.warning(f"{coin} No UTXOs found")
        return

    utxo_chunks = chunkify(utxos, 800)
    for utxos in utxo_chunks:
        inputs_data = get_inputs(utxos, [])
        inputs = inputs_data[0]
        # Assuming 100 bytes per input
        tx_size = len(inputs) * 100
        value = inputs_data[1]
        vouts = get_vouts(coin, address, value, tx_size)
        if len(inputs) > 0 and len(vouts) > 0:
            print(f"{coin} consolidating {len(inputs)} UTXOs, value: {value}")
            daemon = DaemonRPC(coin)
            txid = daemon.process_raw_transaction(address, utxos, inputs, vouts)
            if txid != "":
                explorer_url = daemon.get_explorer_url(txid, 'tx')
                if explorer_url != "":
                    txid = explorer_url
                print(f"{coin} Sent {value} to {address}: {txid} from {len(inputs)} input UTXOs")
            else:
                logger.error(f"{coin} Failed to send {value} to {address} from {len(inputs)} input UTXOs")
            time.sleep(0.1)
        else:
            logger.debug(f"{coin} no valid inputs or vouts for")

if __name__ == "__main__":
    coins = list(INSIGHT_EXPLORERS.keys())
    coins.sort()
    pubkey = input("Enter local daemon pubkey: ")
    address = input("Enter destination address: ")
    for coin in coins:
        sweep(coin, pubkey, address)
