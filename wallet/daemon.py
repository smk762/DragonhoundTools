#!/usr/bin/env python3
import os
import re
import sys
import json
import time
import const
import helper
import requests
from slickrpc import Proxy
from requests.auth import HTTPBasicAuth
from requests.exceptions import InvalidURL, RequestException, ConnectionError

from logger import logger
from color import ColorMsg

class DaemonRPC():
    def __init__(self, coin):
        self.msg = ColorMsg()
        self.coin = coin
        self.conf_path = helper.get_conf_path(coin)
        self.creds = self.get_creds()
        self.rpcuser = self.creds[0]
        self.rpcpass = self.creds[1]
        self.rpcport = self.creds[2]
        
        
    def get_creds(self):
        rpcport = 0
        rpcuser = ''
        rpcpassword = ''
        if not os.path.exists(self.conf_path):
            pass
        else:
            with open(self.conf_path, 'r') as f:
                for line in f:
                    l = line.rstrip()
                    if re.search('rpcuser', l):
                        rpcuser = l.replace('rpcuser=', '')
                    elif re.search('rpcpassword', l):
                        rpcpassword = l.replace('rpcpassword=', '')
                    elif re.search('rpcport', l):
                        rpcport = int(l.replace('rpcport=', ''))
            if rpcport == 0:
                self.msg.error(f"rpcport not in {self.conf_path}")
        return [rpcuser, rpcpassword, rpcport]

        
    def rpc(self, method: str, method_params: object=None) -> dict:
        if not method_params:
            method_params = []
        params = {
            "jsonrpc": "1.0",
            "id":"curltest",
            "method": method,
            "params": method_params,
        }
        try:
            r = requests.post(
                f"http://127.0.0.1:{self.rpcport}",
                json.dumps(params),
                auth=HTTPBasicAuth(self.rpcuser, self.rpcpass),
                timeout=90
            )
            # logger.debug(f"RPC: {method} {method_params}")
            resp = r.json()
            # logger.debug(f"response: {resp}")
            return resp
        except requests.exceptions.InvalidURL as e:
            resp = {
                "error": "Invalid URL",
                "result": None
            }
            self.msg.error(f'')
        except requests.exceptions.ConnectionError:
            resp = {
                "error": "Daemon connection error",
                "result": None
            }
            self.msg.error(f'')
        except requests.exceptions.RequestException as e:
            resp = {
                "error": f"Error! {e}",
                "result": None
            }
            self.msg.error(f'')
        except Exception as e:
            resp = {
                "error": f"Error! {e}",
                "result": None
            }
        # self.msg.darkgrey(f"RPC Failed: {resp}")
        return resp

    def addnode(self, ip: str, cmd: str="add") -> dict:
        try:
            return self.rpc("addnode", [ip, cmd])["result"]
        except Exception as e:
            return {"error": f"Error! {e}"}

    def getinfo(self):
        return self.rpc("getinfo")["result"]

    def getnetworkinfo(self):
        return self.rpc("getnetworkinfo")["result"]

    def getbalance(self):
        return self.rpc("getbalance")["result"]

    def dumpprivkey(self, address):
        return self.rpc("dumpprivkey", [address])["result"]

    def sendtoaddress(self, address: str, amount: float, subtractfeefromamount: bool=True):
        if not subtractfeefromamount:
            return self.rpc("sendtoaddress", [address, amount])["result"]
        return self.rpc("sendtoaddress", [address, amount, "", "", True])["result"]

    def gettxoutproof(self, txid):
        return self.rpc("gettxoutproof", [[txid]])["result"]

    def importprunedfunds(self, raw_tx, txoutproof):
        return self.rpc("importprunedfunds", [raw_tx, txoutproof])["result"]

    def createrawtransaction(self, inputs, vouts):
        print(f"input: {inputs[0]}")
        print(f"vouts: {vouts[0]}")
        return self.rpc("createrawtransaction", [inputs, vouts])["result"]

    def signrawtransaction(self, unsignedhex):
        return self.rpc("signrawtransaction", [unsignedhex])["result"]

    def signrawtransactionwithwallet(self, unsignedhex):
        return self.rpc("signrawtransactionwithwallet", [unsignedhex])["result"]

    def sendrawtransaction(self, signedhex):
        return self.rpc("sendrawtransaction", [signedhex])["result"]

    def getrawtransaction(self, txid):
        return self.rpc("getrawtransaction", [txid])["result"]

    def importprivkey(self, pk, rescan=False, height=None):
        if height:
            # Not all coins support this, but it mimght come in handy later
            return self.rpc("importprivkey", [pk, "", rescan, height])["result"]
        return self.rpc("importprivkey", [pk, "", rescan])["result"]

    def stop(self):
        return self.rpc("stop")["result"]

    def get_wallet_addr(self):
        resp = self.rpc("listaddressgroupings")["result"]
        addr = None
        if len(resp) > 0:
            addr = resp[0][0][0]
        return addr

    def validateaddress(self, address: str) -> dict:
        data = self.rpc("validateaddress", [address])
        if "result" in data:
            return data["result"]
        logger.debug(f"validateaddress: {data}")
        return {}
    
    def getaddressinfo(self, address: str) -> dict:
        data =  self.rpc("getaddressinfo", [address])
        if "result" in data:
            return data["result"]
        logger.debug(f"getaddressinfo: {data}")
        return {}

    ## Blocks
    def getblock(self, block) -> dict:
        return self.rpc("getblock", [f"{block}"])["result"]
    
    def is_responding(self) -> dict:
        return self.rpc("getblockcount")
    
    def getblockcount(self) -> int:
        return self.rpc("getblockcount")["result"]

    def getblockhash(self, height: int) -> dict:
        return self.getblock(height)["hash"]

    def block_tx(self, height: int) -> dict:
        return self.getblock(height)["tx"]
    
    def last_block_time(self, height) -> int:
        if self.coin in ["LTC", "AYA", "EMC2", "MIL", "CHIPS"]:
            hash = self.getbestblockhash()
            blockinfo = self.getblock(hash)
            blocktime = blockinfo["time"]
        else:
            blocktime = self.block_time(height)
        return blocktime
        
    def block_time(self, height: int) -> int:
        blockinfo = self.getblock(height)
        try:
            return blockinfo["time"]
        except:
            return 0

    def getbestblockhash(self) -> str:
        return self.rpc("getbestblockhash")["result"]

    # Wallet
    def listunspent(self) -> dict:
        return self.rpc("listunspent")["result"]
    
    def rescanblockchain(self, start=1, end=None) -> dict:
        # TODO: AYA uses this, not sure which other chains.
        # Can be used to scan for transactions after importing 
        # a private key without rescan
        if end is None:
            end = self.getblockcount()
        return self.rpc("rescanblockchain", [start, end])["result"]

    def unlock_unspent(self, locked_unspent):
        return self.rpc("lockunspent", [True, locked_unspent])["result"]

    def listlockunspent(self):
        return self.rpc("listlockunspent")["result"]

    # Transactions
    def listtransactions(self, count: int=99999999) -> dict:
        return self.rpc("listtransactions", ["*", count])["result"]

    # Mining
    def setgenerate(self, mining=True, cores=1):
        return self.rpc("setgenerate", [mining, cores])["result"]

    # komodo-cli lockunspent true "[{\"txid\":\"a08e6907dbbd3d809776dbfc5d82e371b764ed838b5655e72f463568df1aadf0\",\"vout\":1}]"
    def get_unspendable(self, unspent):
        # TODO: Unused, remove?
        for utxo in unspent:
            if not utxo["spendable"]:
                logger.info(utxo)

    def get_explorer_url(self, value, endpoint: str='tx') -> str:
        # Param value can be a txid, address, or block
        # Valid endpoint values: explorer_tx_url, explorer_address_url, TODO: explorer_block_url (needs to be added to coins repo)
        if self.coin in const.INSIGHT_EXPLORERS:
            if const.INSIGHT_EXPLORERS[self.coin] != "":
                if endpoint == "tx":
                    endpoint = "tx/"
                elif endpoint == "addr":
                    endpoint = "address/"
                elif endpoint == "block":
                    endpoint = "block/"
                return f"{const.INSIGHT_EXPLORERS[self.coin]}{endpoint}{value}"
        elif self.coin in const.CRYPTOID_EXPLORERS:
            baseurl = f"https://chainz.cryptoid.info/emc2/"
            if endpoint == "tx":
                return f"{baseurl}tx.dws?{value}.htm"
            elif endpoint == "addr":
                return f"{baseurl}address.dws?{value}.htm"
            elif endpoint == "block":
                return f"{baseurl}block.dws?{value}.htm"
            
        elif self.coin in const.BLOCKCYPHER_EXPLORERS:
            baseurl = f"https://live.blockcypher.com/{self.coin.lower()}/"
            if endpoint == "tx":
                return f"{baseurl}tx/{value}"
            elif endpoint == "addr":
                return f"{baseurl}address/{value}"
            elif endpoint == "block":
                return f"{baseurl}block/{value}"
            
        try:
            coin = self.coin.split("_")[0]
            if coin == "TOKEL":
                coin = "TKL"
            elif coin == "PIRATE":
                coin = "ARRR"
            else:
                coin = self.coin
            data = helper.get_coins_config()
            baseurl = data[coin]["explorer_url"]
            if endpoint == "tx":
                if "explorer_tx_url" in data[coin]:
                    endpoint = data[coin]["explorer_tx_url"]
                if endpoint == "":
                    endpoint = "tx/"
            if endpoint == "addr":
                if "explorer_address_url" in data[coin]:
                    endpoint = data[coin]["explorer_address_url"]
                if endpoint == "":
                    endpoint = "addr/"
            if endpoint == "block":
                # Needs more suport in coins repo
                endpoint = "b/"
            return f"{baseurl}{endpoint}{value}"
        except json.decoder.JSONDecodeError:
            return ""
        except Exception as e:
            logger.error(f"Error getting explorers: {e}")
            return ""

    def get_utxo_count(self, utxo_value: float) -> int:
        unspent = self.listunspent()
        count = 0
        if unspent:
            for utxo in unspent:
                if utxo["amount"] == utxo_value:
                    count += 1
        return count

    def is_mining(self) -> bool:
        try:
            if "result" in self.rpc("getmininginfo"):
                if "generate" in self.rpc("getmininginfo")["result"]:
                    return self.rpc("getmininginfo")["result"]["generate"]
        except Exception as e:
            pass
        return False

    def start_mining(self) -> bool:
        return self.rpc("setgenerate", [True, 1])["result"]

    def stop_mining(self) -> bool:
        return self.rpc("setgenerate", [False])["result"]


    def process_raw_transaction(self, address: str, utxos: list, inputs: list, vouts: dict) -> str:
        unsignedhex = self.createrawtransaction(inputs, vouts)

        # Some coins dont allow signrawtransaction,
        # others dont have signrawtransactionwithwallet.
        # So we try both
        signedhex = self.signrawtransaction(unsignedhex)
        if signedhex is None:
            signedhex = self.signrawtransactionwithwallet(unsignedhex)
        if signedhex is None:
            logger.error(f"{self.coin} Could not signrawtransaction")
            #logger.debug(f"{self.coin} inputs {inputs}")
            #logger.debug(f"{self.coin} vouts {vouts}")
            logger.debug(f"{self.coin} unsignedhex {unsignedhex}")
            return ""
        time.sleep(0.1)
        txid = self.sendrawtransaction(signedhex["hex"])

        if txid is not None:
            return txid
        # Remove error utxos and retry
        if not signedhex['complete']:
            if 'errors' in signedhex:
                errors = signedhex['errors']
                error_utxos = []
                for error in errors:
                    if error['error'] == 'Input not found or already spent':
                        error_utxos.append({"txid": error['txid'], "vout": error['vout']})
                    elif error['error'] == 'Operation not valid with the current stack size':
                        error_utxos.append({"txid": error['txid'], "vout": error['vout']})
                    logger.debug(f"Removing spent utxo: {error['txid']}:{error['error']}")
                if len(error_utxos) == len(inputs):
                    logger.debug(f"All utxos errored, wont send.")
                elif len(error_utxos) > 0:
                    logger.debug(f"Removing {len(error_utxos)} Error UTXOs to try again...")
                    inputs_data = self.get_inputs(utxos, error_utxos)
                    inputs = inputs_data[0]
                    value = inputs_data[1]
                    tx_size = len(inputs) * 100
                    vouts = self.get_vouts(self.coin, address, value, tx_size)
                    if len(inputs) > 0 and len(vouts) > 0:
                        try:
                            txid = self.process_raw_transaction(address, utxos, inputs, vouts)
                            if txid != "":
                                explorer_url = self.get_explorer_url(txid, 'tx')
                                if explorer_url != "":
                                    txid = explorer_url
                                self.msg.info(f"Sent {value} to {address}: {txid}")
                            else:
                                logger.error(f"Failed to send {value} to {address}")
                        except Exception as e:
                            logger.error(e)
                        time.sleep(0.1)
                    else:
                        logger.debug(f"Nothing to send!")
        logger.error(f"{self.coin} Failed with signedhex {signedhex}")
        #logger.error(f"{self.coin} inputs {inputs}")
        #logger.error(f"{self.coin} vouts {vouts}")
        return ""