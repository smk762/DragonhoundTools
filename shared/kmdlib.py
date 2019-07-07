#!/usr/bin/env python3
import os
import re
import sys
import json
import http
import time
import codecs
import platform
from slickrpc import Proxy
from os.path import expanduser
home = expanduser("~")
operating_system = platform.system()

with open(home+"/dragonhoundTools/config/config.json") as j:
  config_json = json.load(j)

iguanaport = config_json['iguanaport']
nn_Radd = config_json['nn_Radd']
komodo_ac_json = config_json['komodo_ac_json']
labs_ac_json = config_json['labs_ac_json']

# Change here to use for LABS
coins_json = home+'/'+komodo_ac_json
#coins_json = home+'/'+labs_ac_json

if operating_system == 'Darwin':
    ac_dir = home + '/Library/Application Support/Komodo'
elif operating_system == 'Linux':
    ac_dir = home + '/.komodo'
elif operating_system == 'Win64' or operating_system == 'Windows':
    ac_dir = '%s/komodo/' % os.environ['APPDATA']
    import readline


def colorize(string, color):
    colors = {
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'green': '\033[92m',
        'red': '\033[91m'
    }
    if color not in colors:
        return string
    else:
        return colors[color] + string + '\033[0m'

def def_creds(chain):
    rpcport ='';
    if chain == 'KMD':
        coin_config_file = str(ac_dir + '/komodo.conf')
    else:
        coin_config_file = str(ac_dir + '/' + chain + '/' + chain + '.conf')
    with open(coin_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('rpcuser', l):
                rpcuser = l.replace('rpcuser=', '')
            elif re.search('rpcpassword', l):
                rpcpassword = l.replace('rpcpassword=', '')
            elif re.search('rpcport', l):
                rpcport = l.replace('rpcport=', '')
    if len(rpcport) == 0:
        if chain == 'KMD':
            rpcport = 7771
        else:
            print("rpcport not in conf file, exiting")
            print("check "+coin_config_file)
            exit(1)
    return(Proxy("http://%s:%s@127.0.0.1:%d"%(rpcuser, rpcpassword, int(rpcport))))

def coins_info(coins_json_file, attrib='ac_name'):
        infolist = []
        with open(coins_json_file) as file:
            assetchains = json.load(file)
        for chain in assetchains:
            infolist.append(chain[attrib])
        return infolist

def wait_confirm(coin, txid):
    start_time = time.time()
    while txid in rpc[coin].getrawmempool():
        print("Waiting for confirmation...")
        time.sleep(15)
        looptime = time.time() - start_time
        if looptime > 900:
            print("Transaction timed out")
            return False
    print("Transaction "+txid+" confirmed!")
    return True

def send_confirm_rawtx(coin, hexstring):
    start_time = time.time()
    txid = rpc[coin].sendrawtransaction(hexstring)
    print(hexstring)
    print(txid)
    while len(txid) != 64:
        print("Sending raw transaction...")
        txid = rpc[coin].sendrawtransaction(hexstring)
        print(txid)
        time.sleep(20)
        looptime = time.time() - start_time
        if looptime > 900:
            print("Transaction timed out")
            print(txid)
            exit(1)
    while txid in rpc[coin].getrawmempool():
        print("Waiting for confirmation...")
        time.sleep(20)
        looptime = time.time() - start_time
        if looptime > 900:
            print("Transaction timed out")
            print(rpc[coin].getrawmempool())
            print(rpc[coin].getblockcount())
            exit(1)
    print("Transaction "+txid+" confirmed!")
    return txid

    
def unlockunspent(coin):
        unspent = rpc[coin].listlockunspent()
        rpc[coin].lockunspent(True, unspent)

def unspent_count(coin):
    count = 0
    dust = 0
    unspent = rpc[coin].listunspent()
    for utxo in unspent:
        if utxo['amount'] == 0.0001:
            count += 1
        elif utxo['amount'] < 0.0001:
            dust += 1
    return [count,dust]

def unspent_info(coin):
    count = 0
    dust = 0
    newest = 999999999999999999
    oldest = 0
    interest_utxos = 0 
    interest_value = 0
    unspent = rpc[coin].listunspent()
    for utxo in unspent:
        if utxo['interest'] > 0:
            interest_utxos += 1
            interest_value += utxo['interest']        
        if utxo['confirmations'] > oldest:
            oldest = time_since
        if utxo['confirmations'] < newest:
            newest = time_since
        if utxo['amount'] > largest:
            oldest = time_since
        if utxo['amount'] < smallest:
            newest = time_since
        if utxo['amount'] == 0.0001:
            count += 1
        elif utxo['amount'] < 0.0001:
            dust += 1
    return [count,dust,oldest,newest,interest_utxos,interest_value]

def unspent_interest(coin):
    interest_utxos = 0 
    interest_value = 0
    unspent = rpc[coin].listunspent()
    for utxo in unspent:
        if utxo['interest'] > 0:
            interest_utxos += 1
            interest_value += utxo['interest']
    return [interest_utxos,interest_value]
