#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *


# The BTC and KMD address here must remain the same.
# Do not need to enter yours!
txscanamount = 10080 # one week. If not NTX for this long, something broken!
utxoamt=0.00010000
ntrzdamt=-0.00083600
timefilter2=1525513998


print(\
    "|"+'{:^11}'.format('COIN')+"|"+'{:^9}'.format('BALANCE')+ \
    "|"+'{:^7}'.format('TX')+"|"+'{:^9}'.format('SYNC %')+ \
    "|"+'{:^11}'.format('LAST NTX')+"|"+'{:^9}'.format('24H NTX')+ \
    "|"+'{:^6}'.format('CONN')+ \
    "|")
for coin in coinlist:
    coin_str = '{:^11}'.format(coin) 
    wallet_info = rpc[coin].getwalletinfo()
    balance = '{:^9}'.format(str(wallet_info['balance'])[:7])
    if this_node == 'third_party':
        txcount = '{:^7}'.format(str(len(rpc[coin].listtransactions())))
    else:
        txcount = '{:^7}'.format(str(wallet_info['txcount']))
    blocks = rpc[coin].getbalance()
    longestchain = rpc[coin].getbalance()
    try:
        sync_pct = '{:^9}'.format(str(blocks/longestchain*100)+"%")
    except:
        sync_pct = '{:^9}'.format("N/A")

    last_ntx_time = 0
    ntx_24hr = 0
    txinfo = rpc[coin].listtransactions("", txscanamount)
    now = time.time()
    for tx in txinfo:
        if 'address' in tx:
            if tx['address'] == ntx_Radd:
                if tx['time'] > last_ntx_time:
                    last_ntx_time = int(tx['time'])
                if tx['time'] > now - 86400:
                    ntx_24hr += 1
    time_since_ntx = now-last_ntx_time

    last_ntx = '{:^11}'.format(display_time(time_since_ntx))
    ntx_24hr = '{:^9}'.format(str(ntx_24hr))
    connected = '{:^6}'.format(str(rpc[coin].getnetworkinfo()['connections']))
    print("|"+coin_str+"|"+balance+"|"+txcount+"|"+sync_pct+"|"+last_ntx+"|"+ntx_24hr+"|"+connected+"|")