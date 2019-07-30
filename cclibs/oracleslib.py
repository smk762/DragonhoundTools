#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *

# DOCS: https://developers.komodoplatform.com/basic-docs/antara/antara-api/oracles.html

def create_oracle(coin, oracle_name, oracle_description, oracletype, datafee=10000):
    result = rpc[coin].oraclescreate(str(oracle_name), str(oracle_description), oracletype)
    oracleHex=result['hex']
    oracleResult=result['result']
    while oracleResult != 'success':
        result = rpc[coin].oraclescreate(str(oracle_name), str(oracle_description), oracletype)
        oracleHex=result['hex']
        oracleResult=result['result']
    oracle_txid = rpc[coin].sendrawtransaction(oracleHex)
    memPool = str(rpc[coin].getrawmempool())
    while memPool.find(oracle_txid) < 0:
        time.sleep(15)
        memPool = str(rpc[coin].getrawmempool())
    print("Oracle created. TXID: "+oracle_txid)
    oraclesList = str(rpc[coin].oracleslist())
    while oraclesList.find(oracle_txid) < 0:
        time.sleep(15)
        oraclesList = str(rpc[coin].oracleslist())
    print("Oracle Listing confirmed")
    fund = rpc[coin].oraclesfund(oracle_txid)
    oracleHex=fund['hex']
    oracleResult=fund['result']
    while oracleResult != 'success':
        fund = rpc[coin].oraclesfund(oracle_txid)
        oracleHex=fund['hex']
        oracleResult=fund['result']
    result = rpc[coin].sendrawtransaction(oracleHex)
    while len(result) != 64:
        time.sleep(15)
        result = rpc[coin].sendrawtransaction(oracleHex)
    print("Oracle funded")
    rego = rpc[coin].oraclesregister(oracle_txid, datafee)
    oracleHex=rego['hex']
    oracleResult=rego['result']
    while oracleResult != 'success':
        rego = rpc[coin].oraclesregister(oracle_txid, datafee)
        oracleHex=rego['hex']
        oracleResult=rego['result']
    rego_hex = rpc[coin].sendrawtransaction(oracleHex)
    while len(rego_hex) != 64:
        time.sleep(15)
        rego_hex = rpc[coin].sendrawtransaction(oracleHex)
    memPool = str(rpc[coin].getrawmempool())
    while memPool.find(rego_hex) < 0:
        time.sleep(15)
        memPool = str(rpc[coin].getrawmempool())
    print("Oracle registered")
    orcl_info = rpc[coin].oraclesinfo(oracle_txid)
    reg_json=orcl_info['registered']
    while len(reg_json) < 1:
        time.sleep(30)
        orcl_info = rpc[coin].oraclesinfo(oracle_txid)
        reg_json=orcl_info['registered']
    publisher=str(orcl_info['registered'][0]['publisher'])
    amount = 10
    for i in range (0,10):
        result = rpc[coin].oraclessubscribe(oracle_txid, publisher, str(amount))
        orcl_hex = result['hex']
        rpc[coin].sendrawtransaction(orcl_hex)
    return oracle_txid

def register_oracle(coin, oracletxid, datafee):
    datafee=str(datafee)
    pubkey = rpc[coin].getinfo()['pubkey']
    rego = rpc[coin].oraclesregister(oracletxid, datafee)
    if rego['result'] == 'error':
        print(colorize(rego['error'], 'red'))
        exit(1)
    oracleHex=rego['hex']
    oracleResult=rego['result']
    while oracleResult != 'success':
        rego = rpc[coin].oraclesregister(oracletxid, datafee)
        oracleHex=rego['hex']
        oracleResult=rego['result']
    regotx = rpc[coin].sendrawtransaction(oracleHex)
    print(colorize('sending oracle registration tx', 'blue'))
    while len(regotx) != 64:
        time.sleep(15)
        regotx = rpc[coin].sendrawtransaction(oracleHex)  
        print(colorize('sending oracle registration tx', 'blue'))    
    memPool = str(rpc[coin].getrawmempool())
    while memPool.find(regotx) < 0:
        time.sleep(5)
        memPool = str(rpc[coin].getrawmempool())
    orcl_info = rpc[coin].oraclesinfo(oracletxid)
    reg_json=orcl_info['registered']
    while len(reg_json) < 1:
        print(colorize('waiting for oracle registration', 'blue'))
        time.sleep(15)
        orcl_info = rpc[coin].oraclesinfo(oracletxid)
        reg_json=orcl_info['registered']
    for reg_pub in reg_json:
        if reg_pub['publisher'] == pubkey:
            publisher=str(reg_pub['publisher'])
            funds=str(reg_pub['funds'])
            print(colorize("publisher ["+publisher+"] registered on oracle ["+oracletxid+"]!", 'green'))
    return publisher

def fund_oracle(coin, oracletxid, publisher, funds):
    pubkey = rpc[coin].getinfo()['pubkey']
    orcl_info = rpc[coin].oraclesinfo(oracletxid)
    reg_json=orcl_info['registered']
    for reg_pub in reg_json:
        if reg_pub['publisher'] == pubkey:
            exisingFunds=float(reg_pub['funds'])
    amount = float(funds)/10;
    sub_transactions = []
    for x in range(1,11):
        subtx = ''
        while len(subtx) != 64:
            print(colorize("Sending funds "+str(x)+"/10 to oracle", 'blue'))
            subHex = rpc[coin].oraclessubscribe(oracletxid, publisher, str(amount))['hex']
            subtx = rpc[coin].sendrawtransaction(subHex)
            time.sleep(5)
        sub_transactions.append(subtx)
        print(colorize("Funds "+str(x)+"/10 sent to oracle", 'blue'))
    while exisingFunds < 1:
        orcl_info = rpc[coin].oraclesinfo(oracletxid)
        reg_json=orcl_info['registered']
        for reg_pub in reg_json:
            if reg_pub['publisher'] == pubkey:
                exisingFunds=float(reg_pub['funds'])
        print(colorize("waiting for funds to appear on oracle",'blue'))
        time.sleep(15)
    print(colorize("Finished sending "+str(funds)+" to oracle.", 'green'))

def write2oracle(coin, oracletxid, message):
    rawhex = codecs.encode(message).hex()
    bytelen = int(len(rawhex) / int(2))
    hexlen = format(bytelen, 'x')
    if bytelen < 16:
        bigend = "000" + str(hexlen)
    elif bytelen < 256:
        bigend = "00" + str(hexlen)
    elif bytelen < 4096:
        bigend = "0" + str(hexlen)
    elif bytelen < 65536:
        bigend = str(hexlen)
    else:
        print("message too large, must be less than 65536 characters")
    lilend = bigend[2] + bigend[3] + bigend[0] + bigend[1]
    fullhex = lilend + rawhex
    oraclesdata_result = rpc[coin].oraclesdata(oracletxid, fullhex)
    result = oraclesdata_result['result']
    if result == 'error':
        print('ERROR:' + oraclesdata_result['error'] + ', try using oraclesregister if you have not already, and check the oracle is funded')
    else:
        rawtx = oraclesdata_result['hex']
        sendrawtransaction_result = rpc[coin].sendrawtransaction(rawtx)
    print(colorize("Message ["+message+"] written to oracle.", 'green'))
    return result

def read_oracle(coin, oracletxid, numrec):
    pubkey = rpc[coin].getinfo()['pubkey']
    orcl_info = rpc[coin].oraclesinfo(oracletxid)
    reg_json=orcl_info['registered']
    for reg_pub in reg_json:
        if reg_pub['publisher'] == pubkey:
            batonutxo=reg_pub['batontxid']
    if 'batonutxo' in locals():
        samples = rpc[coin].oraclessamples(oracletxid, batonutxo, str(numrec))
        print(colorize("ERROR: Oracle records retrieved.", 'red'))
        return samples['samples']
    else:
        print(colorize("ERROR: Oracle batonuto does not exist.", 'red'))

def check_oracleFunds(coin, oracletxid, pubkey):
    oraclesinfo = rpc[coin].oraclesinfo(oracletxid)
    publishers = []
    funds = 0
    timeout = 0
    while funds < 1:
        oraclesinfo = rpc[coin].oraclesinfo(oracletxid)
        for pub in oraclesinfo['registered']:
            publishers.append(pub['publisher'])
        if pubkey in publishers:
            for pub in oraclesinfo['registered']:
                if pub['publisher'] == pubkey:
                    funds = float(pub['funds'])
        timeout += 1
        if timeout > 12:
            print("Oracle funding timed out :(")
            sys.exit(1)
        time.sleep(20)
    
def add_oracleFunds(coin, oracletxid, pubkey):
    oe_bal = rpc[coin].getbalance()
    if oe_bal < 100:
        print(coin+" balance: "+str(oe_bal)+" (need > 100)")
        print("Your "+coin+" balance needs a top up!")
        print("Ask @smk762#7640 on Discord to send some.")
        sys.exit(1)
    else:
        print("Adding funds to your "+coin+" subscription...")
        for x in range(10):
            result = rpc[coin].oraclessubscribe(oracletxid, pubkey, str(10))
            orcl_hex = result['hex']
            rpc[coin].sendrawtransaction(orcl_hex)

