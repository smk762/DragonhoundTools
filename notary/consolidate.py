#!/usr/bin/env python3
import os
import sys
import glob
import time
import json
import requests
import subprocess
import bitcoin # pip3 install python-bitcoinlib
from bitcoin.core import x
from bitcoin.core import CoreMainParams
from bitcoin.wallet import P2PKHBitcoinAddress
from dotenv import load_dotenv
import lib_rpc

load_dotenv()

SWEEP_ADDRESS = os.getenv("SWEEP_ADDRESS")
NN_PRIVKEY = os.getenv("NN_PRIVKEY")

class KMD_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 60,
                       'SCRIPT_ADDR': 85,
                       'SECRET_KEY': 188}

class NotaryNode:
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.assetchains = self.get_assetchains()
        self.coins = [i["ac_name"] for i in self.assetchains] 
        self.coins.append("KMD")
        self.coins_data = self.calc_coins_data()
        self.iguana_dir = f"{self.home}/dPoW/iguana"
        self.log_path = f"{self.home}/logs"
        self.pubkey = self.get_pubkey()
        self.address = self.get_address(self.pubkey)
        self.launch_params = self.get_launch_params()

    def get_assetchains(self):
        with open(f"{self.home}/dPoW/iguana/assetchains.json") as file:
            return json.load(file)

    def calc_coins_data(self):
        coins_data = {}
        for coin in self.coins:
            if coin == "KMD": wallet = f"{self.home}/.komodo/wallet.dat"
            else: wallet = f"{self.home}/.komodo/{coin}/wallet.dat"
            if coin not in coins_data:
                coins_data.update({coin: {}})
            coins_data[coin].update({
                "height": self.get_blockheight(coin),
                "wallet": wallet
            })
        return coins_data

    def get_pubkey(self):
        with open(f"{self.iguana_dir}/pubkey.txt") as f:
            return f.read().replace("pubkey=", "").strip()

    def get_address(self, pubkey):
        bitcoin.params = KMD_CoinParams
        return str(P2PKHBitcoinAddress.from_pubkey(x(pubkey)))

    def get_blockheight(self, coin):
        try:
            rpc = lib_rpc.def_credentials(coin)
            return rpc.getblockcount()
        except Exception as e:
            return None

    def import_pk(self, coin):
        rpc = lib_rpc.def_credentials(coin)
        height = self.coins_data[coin]["height"]
        if not height:
            height = self.get_blockheight(coin)
        return rpc.importprivkey(NN_PRIVKEY, "", True, height)

    def format_param(self, param, value):
        return '-' + param + '=' + value

    def write_coins_data(self, coins_data):
        with open("coins_data.json", "w") as f:
            f.write(json.dumps(coins_data, indent=4))

    def read_coins_data(self):
        with open("coins_data.json", "r") as f:
            return json.loads(f)

    def get_launch_params(self):
        launch_params = {}
        for i in self.assetchains:
            params = []
            for param, value in i.items():
                if isinstance(value, list):
                    for dupe_value in value:
                        params.append(self.format_param(param, dupe_value))
                else:
                    params.append(self.format_param(param, value))
            launch_params.update({i["ac_name"]: " ".join(params)})
        launch_params.update({"KMD": f"-minrelaytxfee=0.000035 -opretmintxfee=0.004 -notary={self.home}/.litecoin/litecoin.conf"})
        return launch_params

    def start_chain(self, coin):
        rpc = lib_rpc.def_credentials(coin)
        params = self.launch_params[coin]
        # check if already running
        try:
            block_height = self.get_blockheight(coin)
            return
        except requests.exceptions.RequestException as e:
            pass
        launch = f"{self.home}/komodo/src/komodod {params} -whitelistaddress={self.address} -pubkey={self.pubkey}"
        log_output = open(f"{self.log_path}/{coin}_daemon.log",'w+')
        subprocess.Popen(launch, stdout=log_output, stderr=log_output, universal_newlines=True)
        time.sleep(3)
        print('{:^60}'.format( f"{coin} daemon starting."))
        print('{:^60}'.format( f"Use 'tail -f {coin}_daemon.log' for mm2 console messages."))
        self.wait_for_start(coin)

    def wait_for_start(self, coin):
        i = 0
        rpc = lib_rpc.def_credentials(coin)
        while True:
            try:
                i += 1
                if i == 15:
                    print(f"Looks like there might be an issue with loading {coin}...")
                    print(f"We'll try and start it again, but  you need it here are the launch params to do it manually:")
                    print(' '.join(self.get_launch_params(coin)))
                    # TODO: Send an alert if this happens
                    return False
                print(f"Waiting for {coin} daemon to restart...")
                time.sleep(30)
                block_height = self.get_blockheight(coin)
                if block_height:
                    return True
            except:
                pass

    def stop(self, coin):
        rpc = lib_rpc.def_credentials(coin)
        try:
            rpc.stop()
            self.wait_for_stop(coin)
        except Exception as e:
            print(e)


    def wait_for_stop(self, coin):
        i = 0
        rpc = lib_rpc.def_credentials(coin)
        while True:
            try:
                i += 1
                if i == 15:
                    print(f"Looks like there might be an issue with stopping {coin}...")
                    # TODO: Send an alert if this happens
                    return False

                print(f"Waiting for {coin} daemon to stop...")
                time.sleep(15)
                block_height = self.get_blockheight(coin)
            except requests.exceptions.RequestException as e:
                return True
        time.sleep(10)

    def consolidate(self, coin):
        rpc = lib_rpc.def_credentials(coin)

        # get a utxo
        url = f"http://stats.kmd.io/api/tools/pubkey_utxos/?coin={coin}&pubkey={self.pubkey}"
        r = requests.get(url)
        utxos = r.json()["results"]["utxos"]
        inputs = []
        value = 0
        remaining_inputs = len(utxos)
        merge_amount = 800
        print(f"consolidating {coin}...")
        if coin == "KMD": address = SWEEP_ADDRESS
        else: address = self.address
        if len(utxos) > 50:
            print(f"Less than 50 UTXOs to consolidate {coin}")
            return
        for utxo in utxos:
            if utxo["confirmations"] < 100:
                remaining_inputs -= 1
                continue
            input_utxo = {"txid": utxo["txid"], "vout": utxo["vout"]}
            inputs.append(input_utxo)
            value += utxo["amount"]

            if len(inputs) > merge_amount or len(inputs) == remaining_inputs:
                remaining_inputs -= merge_amount
                vouts = {address: int(value)-1}
                if coin == "KMD":
                    if int(value) > 0.1:
                        vouts.update({
                            SWEEP_ADDRESS: int(value) - 0.1,
                            self.address: 0.1
                        })
                    else: return
                else:
                    vouts = {self.address: int(value)}

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

        def move_wallet():
            wallet = self.coins_data[coin]["wallet"]
            wallet_bk = wallet.replace("wallet.dat", f"wallet_{now}.dat")
            os.rename(wallet, wallet_bk)





if __name__ == '__main__':

    # For a refresh:
    # - blocks: to get chain blockheights
    # - Stop: stops chains
    # - Move wallets
    # - Start chains
    # - import: Import privkey from blocks info
    # - all: Consolidates funds, sweeps KMD

    node = NotaryNode()
    print(f"Pubkey: {node.pubkey}")
    print(f"Address: {node.address}")
    print(f"Coins: {node.coins}")
    print(f"Coins data: {node.coins_data}") 


    if len(sys.argv) == 2:

        if sys.argv[1] == "backup_wallets":
            now = int(time.time())
            for coin in node.coins:
                node.move_wallet(coin, now)

        elif sys.argv[1] == "stop":
            for coin in node.coins:
                address = node.stop(coin)

        elif sys.argv[1] == "start":
            for coin in node.coins:
                address = node.start_chain(coin)

        elif sys.argv[1] == "import":
            for coin in node.coins:
                address = node.import_pk(coin)

        elif sys.argv[1] == "refresh":
            for coin in node.coins:
                node.get_blockheight(coin)
                node.stop(coin)
                node.move_wallet(coin)
                node.start(coin)
                node.import_pk(coin)
                node.consolidate(coin)
        else:
            print("Invalid option. Use 'backup_wallets', 'stop', 'import', or 'refresh'")
    else:
        for coin in node.coins:
            print(f"Consolidating {coin}...")
            try:
                node.consolidate(coin)
            except Exception as e:
                print(e)
