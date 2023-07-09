#!/usr/bin/env python3
import os
import re
import requests
import json
import platform
import pprint
from datetime import datetime as dt
from slickrpc import Proxy

# sudo apt-get install -y python-pycurl
# slick-bitcoinrpc==0.1.4


NTX_ADDR = "MVx1hSH9WqwQurgqR7HBDRCu3ESkuhQC8r"
#"MGRswY2opYCwGLXxBosyYVbwkVRn1K7dXu"
# define data dir
def get_data_dir():
    operating_system = platform.system()
    if operating_system == 'Darwin':
        ac_dir = os.environ['HOME'] + '/Library/Application Support/mil'
    elif operating_system == 'Linux':
        ac_dir = os.environ['HOME'] + '/.mil'
    elif operating_system == 'Windows':
        ac_dir = '%s/mil/' % os.environ['APPDATA']
    return(ac_dir)

# fucntion to define rpc_connection
def def_credentials():
    rpcport = '';
    data_dir = get_data_dir()
    coin_config_file = str(f"{data_dir}/mil.conf")
    with open(coin_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('rpcuser', l):
                rpcuser = l.replace('rpcuser=', '')
            elif re.search('rpcpassword', l):
                rpcpassword = l.replace('rpcpassword=', '')
            elif re.search('rpcport', l):
                rpcport = l.replace('rpcport=', '')
        return (Proxy("http://%s:%s@127.0.0.1:%d" % (rpcuser, rpcpassword, int(rpcport)), timeout=90))

def get_ntx_txids(addr, start, end):
    params = {"addresses": [addr], "start":start, "end":end}
    return RPC["MIL"].getaddresstxids(params)





def get_ntx_data(txid):
    print(txid)
    raw_tx = RPC["MIL"].getrawtransaction(txid,1)
    if 'blocktime' in raw_tx:
        block_hash = raw_tx['blockhash']
        dest_addrs = raw_tx["vout"][0]['scriptPubKey']['addresses']
        if len(dest_addrs) > 0:
            if NTX_ADDR in dest_addrs:
                print(NTX_ADDR)
                block_time = raw_tx['blocktime']
                block_datetime = dt.utcfromtimestamp(block_time)
                this_block_height = raw_tx['height']
                print(raw_tx['vin'])
                if len(raw_tx['vin']) > 1:
                    notary_list, address_list = get_notary_address_lists(raw_tx['vin'])

    return None


def get_notary_address_lists(vin):
    notary_list = []
    address_list = []
    for item in vin:
        if "address" in item:
            address_list.append(item['address'])
            if item['address'] in MIL_ADDRESSES:
                notary = MIL_ADDRESSES[item['address']]
                notary_list.append(notary)
            else:
                notary_list.append(item['address'])
    notary_list.sort()
    return notary_list, address_list


addresses_dict = requests.get("http://stats.kmd.io/api/table/addresses/?season=Season_6&server=Third_Party&coin=MIL").json()["results"]

notary_ntx_count = {}
MIL_ADDRESSES = {}
for i in addresses_dict:
    MIL_ADDRESSES.update({i["address"]: i["notary"]})
    notary_ntx_count.update({i["notary"]: 0})

RPC = {}
RPC["MIL"] = def_credentials()

for addr in MIL_ADDRESSES:
    print(f"{MIL_ADDRESSES[addr]}: {len(get_ntx_txids(addr, 1, 375621))}")


print(RPC["MIL"].getinfo())
ntx_txids = get_ntx_txids(NTX_ADDR, 1, 375621)
print(ntx_txids)


for txid in ntx_txids:
    raw_tx = RPC["MIL"].getrawtransaction(txid,1)
    print(raw_tx)
    if 'blocktime' in raw_tx:
        block_hash = raw_tx['blockhash']
        dest_addrs = raw_tx["vout"][0]['scriptPubKey']['addresses']
        if len(dest_addrs) > 0:
            if NTX_ADDR in dest_addrs:

                block_time = raw_tx['blocktime']
                block_datetime = dt.utcfromtimestamp(block_time)
                this_block_height = raw_tx['height']

                if len(raw_tx['vin']) > 1:
                    notary_list, address_list = get_notary_address_lists(raw_tx['vin'])
                    for notary in notary_list:
                        notary_ntx_count[notary] += 1

print(notary_ntx_count)
