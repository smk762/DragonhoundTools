#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
import lib_rpc
import base58
import bitcoin # pip3 install python-bitcoinlib
from bitcoin.core import x
from bitcoin.core import CoreMainParams
from bitcoin.wallet import P2PKHBitcoinAddress

from dotenv import load_dotenv
load_dotenv()

SWEEP_ADDRESS = os.getenv("SWEEP_ADDRESS")
NN_PRIVKEY = os.getenv("NN_PRIVKEY")


class KMD_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 60,
                       'SCRIPT_ADDR': 85,
                       'SECRET_KEY': 188}


def consolidate(coin, pubkey, address):
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
                #print(f"rawhex: {rawhex}")
                time.sleep(0.1)
                signedhex = rpc.signrawtransaction(rawhex)
                #print(f"signedhex: {signedhex}")
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


def get_coins():
    with open(f"{os.path.expanduser('~')}/dPoW/iguana/assetchains.json") as file:
        return json.load(file)


def get_pubkey():
    rpc = lib_rpc.def_credentials("KMD")
    return rpc.getinfo()["pubkey"]


def get_address(pubkey):
    bitcoin.params = KMD_CoinParams
    return str(P2PKHBitcoinAddress.from_pubkey(x(pubkey)))


def get_wallets():
    for filename in glob.iglob(f"{os.path.expanduser('~')}/.komodo**/wallet.dat", recursive = True):
        print(filename)


def get_blockheight(coin):
    rpc = lib_rpc.def_credentials(coin)
    return rpc.getblockcount()


def write_blocks(blocks):
    with open("blocks.json", "w") as f:
        f.write(json.dumps(blocks, indent=4))


def read_blocks(blocks):
    with open("blocks.json", "r") as f:
        return json.loads(blocks))


def import_pk(coin, height):
    rpc = lib_rpc.def_credentials(coin)
    return rpc.importprivkey(PRIVKEY, "", True, height)


def stop(coin, height):
    rpc = lib_rpc.def_credentials(coin)
    rpc.stop()


def format_param(param, value):
    return '-' + param + '=' + value


def get_launch_params():
    script_dir = os.path.dirname(__file__)
    with open(f"{script_dir}/dPow/iguana/assetchains.json") as file:
        assetchains = json.load(file)
    launch_params = {}
    for coin in assetchains:
        params = []
        for param, value in chain.items():
            if isinstance(value, list):
                for dupe_value in value:
                    params.append(format_param(param, dupe_value))
            else:
                params.append(format_param(param, value))
        launch_params.update({coin: params})
    return launch_params

roxy(coin, "setgenerate", [mining, cores])['result']


def start_chain(coin, pubkey, launch_params):
        params = launch_params[coin]
        # check if already running
        try:
            block_height = getblockcount(coin)
            return
        except requests.exceptions.RequestException as e:
            pass
        launch = f"{os.path.expanduser('~')}/komodo/src/komodod {params} -pubkey={pubkey}"
        log_output = open(f"{coin}_daemon.log",'w+')
        subprocess.Popen(launch_params, stdout=log_output, stderr=log_output, universal_newlines=True, preexec_fn=preexec)
        time.sleep(3)
        print('{:^60}'.format( f"{coin} daemon starting."))
        print('{:^60}'.format( f"Use 'tail -f {coin}_daemon.log' for mm2 console messages."))


def wait_for_stop(coin):
    while True:
        try:
            print(f"Waiting for {coin} daemon to stop...")
            time.sleep(10)
            block_height = getblockcount(coin)
        except requests.exceptions.RequestException as e:
            break
    time.sleep(10)


def wait_for_start(coin):
    i = 0
    while True:
        try:
            i += 1
            if i > 8:
                start_chain(coin)
                print(f"Looks like there might be an issue with loading {coin}...")
                print(f"We'll try and start it again, but  you need it here are the launch params to do it manually:")
                print(' '.join(get_launch_params(coin)))
                i = 0
            print(f"Waiting for {coin} daemon to restart...")
            time.sleep(30)
            block_height = getblockcount(coin)
            print(block_height)
            if block_height:
                return block_height
        except:
            pass




if __name__ == '__main__':

    # For a refresh:
    # - blocks: to get chain blockheights
    # - Stop: stops chains
    # - Move wallets
    # - Start chains
    # - import: Import privkey from blocks info
    # - all: Consolidates funds, sweeps KMD

    if len(sys.argv) == 2:
        if sys.argv[1] == "blocks":
            blocks = {}
            coins = get_coins()
            for coin in coins:
                if coin = "KMD": wallet = f"{os.path.expanduser('~')}/.komodo/wallet.dat"
                else: wallet = f"{os.path.expanduser('~')}/.komodo/{coin}/wallet.dat"
                blocks.update({
                    coin: {
                        "height": get_blockheight(coin),
                        "wallet": wallet
                })
            write_blocks(blocks)

        if sys.argv[1] == "clean_wallet":
            blocks = read_blocks()
            now = int(time.time())
            for coin in blocks:
                 wallet = blocks[coin]["wallet"]
                 wallet_bk = wallet.replace("wallet.dat", f"wallet_{now}.dat")
                 os.rename(wallet, wallet_bk)

        if sys.argv[1] == "stop":
            blocks = read_blocks()
            for coin in blocks:
                address = stop(coin)
                print(f"Stopped {coin}")


        if sys.argv[1] == "import":
            blocks = read_blocks()
            for coin in blocks:
                address = import_pk(coin, blocks[coin]["height"])
                print(f"Imported privkey into {coin} on block {blocks[coin]['height']}: {address}")


        if sys.argv[1] == "all":
            coins = get_coins()
            pubkey = get_pubkey()
            address = get_address(pubkey)
            for coin in coins:
                if coin = "KMD" and SWEEP_ADDRESS:
                    adress = SWEEP_ADDRESS
                print(f"Consolidating | {coin['ac_name']} | {pubkey}  {address}")
                try:
                    consolidate(coin['ac_name'], pubkey, address)
                except Exception as e:
                    print(e)


    elif len(sys.argv) == 4:
        coin = sys.argv[1]
        pubkey = sys.argv[2]
        address = sys.argv[3]
        consolidate(coin, pubkey, address)
    else:
        coin = input("coin: ")
        pubkey = input("pubkey: ")
        address = input("address: ")
        consolidate(coin, pubkey, address)

