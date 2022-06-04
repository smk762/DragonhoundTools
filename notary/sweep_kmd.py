#!/usr/bin/env python3
import os
import sys
import time
import requests
from os.path import expanduser
from dotenv import load_dotenv

import lib_rpc

load_dotenv()

HOME = expanduser("~")
coin = "KMD"
pubkey = os.getenv('NN_PUBKEY')
sweep_address = os.getenv('SWEEP_ADDR')
nn_address = os.getenv('NN_ADDR')

rpc = lib_rpc.def_credentials(coin)

# get a utxo
url = f"http://stats.kmd.io/api/tools/pubkey_utxos/?coin={coin}&pubkey={pubkey}"
r = requests.get(url)
utxos = r.json()["results"]["utxos"]
inputs = []
value = 0
remaining_inputs = len(utxos)
merge_amount = 800

for utxo in utxos:
    if utxo["confirmations"] < 100 or utxo["satoshis"] == 10000:
        remaining_inputs -= 1
        continue
    input_utxo = {"txid": utxo["txid"], "vout": utxo["vout"]}
    inputs.append(input_utxo)
    value += utxo["satoshis"]

    if len(inputs) > merge_amount or len(inputs) == remaining_inputs:
        remaining_inputs -= merge_amount
        vouts = {
            sweep_address: round(value / 100000000, 4) - 1.0001,
            nn_address: 1,
        }

        try:
            rawhex = rpc.createrawtransaction(inputs, vouts)
            print(f"rawhex: {rawhex}")
            time.sleep(0.1)
            signedhex = rpc.signrawtransaction(rawhex)
            print(f"signedhex: {signedhex}")
            time.sleep(0.1)
            txid = rpc.sendrawtransaction(signedhex["hex"])
            print(f"Sent {value / 100000000} to {nn_address}")
            print(f"txid: {txid}")
            time.sleep(0.1)
        except Exception as e:
            print(e)
            print(utxo)
            print(vouts)

        inputs = []
        value = 0
        if remaining_inputs < 0:
            break
        print(f"{remaining_inputs} remaining utxos")
        time.sleep(4)
