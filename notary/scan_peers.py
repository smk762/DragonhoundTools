#!/usr/bin/env python3
import os
import re
import sys
import json
import platform
import datetime
import requests
from slickrpc import Proxy
from dotenv import load_dotenv

# Deps:
# sudo apt-get install libgnutls28-dev python3 python3-pip python3-setuptools python3-six
# pip3 install slick-bitcoinrpc==0.1.4

# Usage:
# ./scan_peers.py [season] [server]
# Returns list of IP addresses from `getpeersinfo` which appear in 4+ chains


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
        return (Proxy(f"http://{rpcuser}:{rpcpassword}@127.0.0.1:{rpcport}", timeout=90))
    except:
        print("Unable to set RPC proxy, please confirm rpcuser, rpcpassword and rpcport are set in "+coin_config_file)

def scan_peers(season, server):
    RPC = {}
    coins = requests.get(f"https://stats.kmd.io/api/info/dpow_server_coins/?season={season}&server={server}").json()["results"]

    for coin in coins:
        RPC.update({coin: def_credentials(coin)})

    peer_ips = {}
    for coin in RPC:
        info = RPC[coin].getpeerinfo()
        for i in info:
            addr = i['addr'].split(':')[0]
            if addr not in peer_ips:
                peer_ips.update({addr:[]})
            if coin not in peer_ips[addr]:
                peer_ips[addr].append(coin)

    with open('peer_ips.json', 'w+') as f:
       json.dump(peer_ips, f, indent=4)

    for addr in peer_ips:
        if len(peer_ips[addr]) > 4:
            print(addr)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        season = sys.argv[1]
        server = sys.argv[2]
    else:
        season = "Season_6"
        server = "Main"

    scan_peers(season, server)
