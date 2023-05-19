#!/usr/bin/env python3
import sys
import time
import requests
import lib_rpc

if len(sys.argv) == 4:
    coin = sys.argv[1]
    pubkey = sys.argv[2]
    address = sys.argv[3]
else:
    coin = input("coin: ")
    pubkey = input("pubkey: ")
    address = input("address: ")


rpc = lib_rpc.def_credentials(coin)

# get a utxo
url = f"http://stats.kmd.io/api/tools/pubkey_utxos/?coin={coin}&pubkey={pubkey}"
r = requests.get(url)
utxos = r.json()["results"]["utxos"]
inputs = []
value = 0
remaining_inputs = len(utxos)
merge_amount = 800
print(f"consolidating {coin}...")
for utxo in utxos:
    if utxo["confirmations"] < 100:
        remaining_inputs -= 1
        continue
    input_utxo = {"txid": utxo["txid"], "vout": utxo["vout"]}
    inputs.append(input_utxo)
    value += utxo["amount"]

    if len(inputs) > merge_amount or len(inputs) == remaining_inputs:
        remaining_inputs -= merge_amount
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
        print(f"{coin} has {remaining_inputs} remaining utxos")
        time.sleep(4)
