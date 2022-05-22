#!/usr/bin/env python3
import time
import requests
import lib_rpc

coin = ""
pubkey = ""
address = ""

rpc = lib_rpc.def_credentials(coin)

# get a utxo
url = f"http://stats.kmd.io/api/tools/pubkey_utxos/?coin={coin}&pubkey={pubkey}"
r = requests.get(url)
utxos = r.json()["results"]["utxos"]
inputs = []
value = 0
for utxo in utxos:
    input_utxo = {"txid": utxo["txid"], "vout": utxo["vout"]}
    inputs.append(input_utxo)
    value += utxo["amount"]

    if len(inputs) > 100:

        vouts = {
            address: int(value),
        }

        try:
            rawhex = rpc.createrawtransaction(inputs, vouts)
            print(f"rawhex: {rawhex}")
            time.sleep(0.1)
            signedhex = rpc.signrawtransaction(rawhex)
            print(f"signedhex: {signedhex}")
            time.sleep(0.1)
            txid = rpc.sendrawtransaction(signedhex["hex"])
            print(f"Sent {value} to {address}")
            print(f"txid: {txid}")
            time.sleep(0.1)
        except Exception as e:
            print(e)
            print(utxo)
            print(vouts)

        inputs = []
        value = 0
        time.sleep(4)
