#!/usr/bin/env python3

import os 
import re
import platform
from slickrpc import Proxy
import sys

# define data dir
def def_data_dir():
    operating_system = platform.system()
    if operating_system == 'Darwin':
        ac_dir = os.environ['HOME'] + '/Library/Application Support/Komodo'
    elif operating_system == 'Linux':
        ac_dir = os.environ['HOME'] + '/.komodo'
    elif operating_system == 'Windows':
        ac_dir = '%s/komodo/' % os.environ['APPDATA']
    return(ac_dir)

# fucntion to define rpc_connection
def def_credentials(chain):
    rpcport = '';
    ac_dir = def_data_dir()
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
            print("check " + coin_config_file)
            exit(1)
    try:
        return (Proxy("http://%s:%s@127.0.0.1:%d" % (rpcuser, rpcpassword, int(rpcport))))
    except:
        print("Unable to set RPC proxy, please confirm rpcuser, rpcpassword and rpcport are set in "+coin_config_file)

chain = input("Which chain to consolidate? ")
addr = input("Destination address? ")

rpc = def_credentials(chain)

unspents = rpc.listunspent()
amount = 0
inputs = []
num_unspents = len(unspents)
tx_fee = 0.0002
tx_size = 1200
i = 1
print("Consolidating "+str(num_unspents)+" utxos")
for unspent in unspents:
    if unspent['confirmations'] > 100 and unspent['spendable'] and unspent['amount'] != 0.0001:
        inputs.append({"txid":unspent['txid'], "vout":unspent['vout']})
        amount += unspent['amount']
        if len(inputs) > tx_size:
            outputs = {addr:amount-tx_fee}
            raw = rpc.createrawtransaction(inputs, outputs)
            signed = rpc.signrawtransaction(raw)
            sent = rpc.sendrawtransaction(signed['hex'])
            amount = 0
            inputs = []
            print("Sent "+str(tx_size*i)+" UTXOs! "+str(num_unspents - tx_size * i)+" remaining...")
            print("TXID: "+sent)
            i += 1
    else:
        print("Skipping "+str(unspent))

outputs = {addr:amount}
raw = rpc.createrawtransaction(inputs, outputs)
signed = rpc.signrawtransaction(raw)
sent = rpc.sendrawtransaction(signed['hex'])
amount = 0
inputs = []
print("TXID: "+sent)



