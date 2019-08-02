#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from statslib import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cclibs'))
from oracleslib import *
now = time.time()
stats_data = []
# The BTC and KMD address here must remain the same.
# Do not need to enter yours!
mining = 0
txscanamount = 10080 # one week. If not NTX for this long, something broken!
ntrzdamt=-0.00083600
timefilter2=1525513998
print("  --------------------------------------------------------------------------------------")    
print(\
    "  |"+'{:^11}'.format('COIN')+"|"+'{:^9}'.format('BALANCE')+ \
    "|"+'{:^6}'.format('UTXO')+"|"+'{:^6}'.format('DUST')+ \
    "|"+'{:^6}'.format('TX')+"|"+'{:^8}'.format('SYNC %')+ \
    "|"+'{:^9}'.format('NTX')+"|"+'{:^6}'.format('24HR')+ \
    "|"+'{:^6}'.format('CONN')+"|"+'{:^8}'.format('MINE')+ \
    "|")
print("  --------------------------------------------------------------------------------------")    
for coin in coinlist:
    if coin == 'GAME' or coin == 'EMC2':
        utxoamt=0.0010000
    else:
        utxoamt=0.00010000
    if coin == 'GAME' or coin == 'GIN':
        ntx_Radd = 'Gftmt8hgzgNu6f1o85HMPuwTVBMSV2TYSt'
    elif coin == 'EMC2':
        ntx_Radd = 'EfCkxbDFSn4X1VKMzyckyHaXLf4ithTGoM'
    elif coin == 'BTC':
        ntx_Radd = '1P3rU1Nk1pmc2BiWC8dEy9bZa1ZbMp5jfg'
    else:
        ntx_Radd = 'RXL3YXG2ceaB6C5hfJcN4fvmLH2C34knhA'
    coin_str = coin
    wallet_info = rpc[coin].getwalletinfo()
    if coin not in ['BTC', 'EMC2', 'GIN', 'GAME']:
        if rpc[coin].getgenerate()['generate'] is True:
            coin_str = coin_str+"*"
    coin_str = '{:^11}'.format(coin_str)
    chaininfo = rpc[coin].getblockchaininfo()
    balance = '{:^9}'.format(str(wallet_info['balance'])[:7])
    txcount = '{:^6}'.format(str(wallet_info['txcount']))
    sync_pct = '{:^8}'.format(str(chaininfo['verificationprogress']*100)[:5]+"%")
    unspent = unspent_count(coin)
    utxos = '{:^6}'.format(str(unspent[0]))
    dust = '{:^6}'.format(str(unspent[1]))
    dif = chaininfo['difficulty']
    last_ntx_time = 0
    last_mined_time = 0
    ntx_24hr = 0
    
    txinfo = rpc[coin].listtransactions("", txscanamount)
    for tx in txinfo:
        if 'address' in tx:
            if tx['address'] == ntx_Radd:
                if tx['time'] > last_ntx_time:
                    last_ntx_time = int(tx['time'])
                if tx['time'] > now - 86400:
                    ntx_24hr += 1
        if 'category' in tx and coin == 'KMD':
            if tx['category'] == 'immature':
                if tx['time'] > last_mined_time:
                    last_mined_time = int(tx['time'])
    time_since_ntx = now-last_ntx_time
    if last_mined_time != 0:
        time_since_mined = now-last_mined_time
        last_mined = '{:^8}'.format(display_time(time_since_mined))
    else:
        last_mined = '{:^8}'.format("N/A")
    last_ntx = '{:^9}'.format(display_time(time_since_ntx))
    
    ntx_24hr = '{:^6}'.format(str(ntx_24hr))
    connected = '{:^6}'.format(str(rpc[coin].getnetworkinfo()['connections']))
    print("  |"+coin_str+"|"+balance+"|" \
              +utxos+"|"+dust+"|" \
              +txcount+"|"+sync_pct+"|" \
              +last_ntx+"|"+ntx_24hr+"|" \
              +connected+"|"+last_mined+"|"\
              +str(dif)+"|")
    json_row = {
                "coin": coin_str.strip(), "bal": balance.strip(), "utxos": utxos.strip(),
                "dust": dust.strip(), "txs": txcount.strip(), "sync": sync_pct.strip(),
                "lastNtx": last_ntx.strip(), "ntx24h": ntx_24hr.strip(),
                "conn": connected.strip()
                }
    stats_data.append(json_row)
print("  --------------------------------------------------------------------------------------")    
publishers = []
stats_json = [{"timestamp": str(now), "data": stats_data }]
try:
    if float(rpc['ORACLEARTH'].getbalance()) < 1:
        print("You have insufficient ORACLEARTH funds to send data")
        print("Ask @smk762#7640 on Discord to send you some.")
        sys.exit(1)
    oracleslist = rpc['ORACLEARTH'].oracleslist()
    if stats_oracletxid in oracleslist:
        oraclesinfo = rpc['ORACLEARTH'].oraclesinfo(stats_oracletxid)
        for pub in oraclesinfo['registered']:
            publishers.append(pub['publisher'])
        if pubkey in publishers:
            for pub in oraclesinfo['registered']:
                if pub['publisher'] == pubkey:
                    funds = float(pub['funds'])
            if funds > 1:
                stats2oracle(rpc['ORACLEARTH'], stats_oracletxid, str(stats_json))
            else:
                add_oracleFunds('ORACLEARTH', stats_oracletxid, pubkey)
                check_oracleFunds('ORACLEARTH', stats_oracletxid, pubkey)
                stats2oracle(rpc['ORACLEARTH'], stats_oracletxid, str(stats_json))
        else:
            print("Your pubkey is not yet registered... will do it now...")
            # oraclesfund
            fund = rpc['ORACLEARTH'].oraclesfund(stats_oracletxid)
            send_confirm_rawtx('ORACLEARTH', fund['hex'])
            print("Oraclesfund confirmed")
            # oraclesregister
            rego = rpc['ORACLEARTH'].oraclesregister(stats_oracletxid, str(1000000))
            send_confirm_rawtx('ORACLEARTH', rego['hex'])
            print("Oracleregister confirmed")
            # oraclessubscribe
            add_oracleFunds('ORACLEARTH', stats_oracletxid, pubkey)
            check_oracleFunds('ORACLEARTH', stats_oracletxid, pubkey)
            print("Oraclessubscribe confirmed")
            write2oracle(rpc['ORACLEARTH'], stats_oracletxid, str(stats_json))
    else:
        print("Oracle not configured.")
        print("Create one at http://oracle.earth")
        print("Then add the txid to ~/DragonhoundTools/config/config.json")
except Exception as e:
    print("ORACLEARTH not running, it can be launched from ~/DragonhoundTools/cc/launch_oe.sh")
