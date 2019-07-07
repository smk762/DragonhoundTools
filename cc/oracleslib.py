#!/usr/bin/env python3
from kmdlib import *

oracletypes = [ 's', 'S', 'd', 'D', 'c', 't', 'i', 'l', 'h', 'Ihh']
def create_oracle(chain, name, description, oracletype):
    rpc_connection = def_credentials(chain)
    if oracletype not in oracletypes:
        errmsg = str(oracletype)+' is not a valid Oracle type. See https://developers.komodoplatform.com/basic-docs/cryptoconditions/cc-oracles.html#oraclescreate for details'
        print(colorize(errmsg, 'red'))
        exit(1)
    result = rpc_connection.oraclescreate(name, description, oracletype)
    oracleHex=result['hex']
    oracleResult=result['result']
    while oracleResult != 'success':
        result = rpc_connection.oraclescreate(name, description, oracletype)
        oracleHex=result['hex']
        oracleResult=result['result']
    oracletxid = rpc_connection.sendrawtransaction(oracleHex)
    while len(oracletxid) != 64:
        time.sleep(15)
        oracletxid = rpc_connection.sendrawtransaction(oracleHex)
    print(colorize("Oracle ["+oracletxid+"] created!", 'green'))
    return oracletxid


def register_oracle(chain, oracletxid, datafee):
    rpc_connection = def_credentials(chain)
    datafee=str(datafee)
    pubkey = rpc_connection.getinfo()['pubkey']
    rego = rpc_connection.oraclesregister(oracletxid, datafee)
    if rego['result'] == 'error':
        print(colorize(rego['error'], 'red'))
        exit(1)
    oracleHex=rego['hex']
    oracleResult=rego['result']
    while oracleResult != 'success':
        rego = rpc_connection.oraclesregister(oracletxid, datafee)
        oracleHex=rego['hex']
        oracleResult=rego['result']
    regotx = rpc_connection.sendrawtransaction(oracleHex)
    print(colorize('sending oracle registration tx', 'blue'))
    while len(regotx) != 64:
        time.sleep(15)
        regotx = rpc_connection.sendrawtransaction(oracleHex)  
        print(colorize('sending oracle registration tx', 'blue'))    
    memPool = str(rpc_connection.getrawmempool())
    while memPool.find(regotx) < 0:
        time.sleep(5)
        memPool = str(rpc_connection.getrawmempool())
    orcl_info = rpc_connection.oraclesinfo(oracletxid)
    reg_json=orcl_info['registered']
    while len(reg_json) < 1:
        print(colorize('waiting for oracle registration', 'blue'))
        time.sleep(15)
        orcl_info = rpc_connection.oraclesinfo(oracletxid)
        reg_json=orcl_info['registered']
    for reg_pub in reg_json:
        if reg_pub['publisher'] == pubkey:
            publisher=str(reg_pub['publisher'])
            funds=str(reg_pub['funds'])
            print(colorize("publisher ["+publisher+"] registered on oracle ["+oracletxid+"]!", 'green'))
    return publisher

def fund_oracle(chain, oracletxid, publisher, funds):
    rpc_connection = def_credentials(chain)
    pubkey = rpc_connection.getinfo()['pubkey']
    orcl_info = rpc_connection.oraclesinfo(oracletxid)
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
            subHex = rpc_connection.oraclessubscribe(oracletxid, publisher, str(amount))['hex']
            subtx = rpc_connection.sendrawtransaction(subHex)
            time.sleep(5)
        sub_transactions.append(subtx)
        print(colorize("Funds "+str(x)+"/10 sent to oracle", 'blue'))
    while exisingFunds < 1:
        orcl_info = rpc_connection.oraclesinfo(oracletxid)
        reg_json=orcl_info['registered']
        for reg_pub in reg_json:
            if reg_pub['publisher'] == pubkey:
                exisingFunds=float(reg_pub['funds'])
        print(colorize("waiting for funds to appear on oracle",'blue'))
        time.sleep(15)
    print(colorize("Finished sending "+str(funds)+" to oracle.", 'green'))

def write2oracle(chain, oracletxid, message):
    rpc_connection = def_credentials(chain)
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
    oraclesdata_result = rpc_connection.oraclesdata(oracletxid, fullhex)
    result = oraclesdata_result['result']
    if result == 'error':
        print('ERROR:' + oraclesdata_result['error'] + ', try using oraclesregister if you have not already, and check the oracle is funded')
    else:
        rawtx = oraclesdata_result['hex']
        sendrawtransaction_result = rpc_connection.sendrawtransaction(rawtx)
    print(colorize("Message ["+message+"] written to oracle.", 'green'))
    return result

def read_oracle(chain, oracletxid, numrec):
    rpc_connection = def_credentials(chain)
    pubkey = rpc_connection.getinfo()['pubkey']
    orcl_info = rpc_connection.oraclesinfo(oracletxid)
    reg_json=orcl_info['registered']
    for reg_pub in reg_json:
        if reg_pub['publisher'] == pubkey:
            batonutxo=reg_pub['batontxid']
    if 'batonutxo' in locals():
        samples = rpc_connection.oraclessamples(oracletxid, batonutxo, str(numrec))
        print(colorize("ERROR: Oracle records retrieved.", 'red'))
        return samples['samples']
    else:
        print(colorize("ERROR: Oracle batonuto does not exist.", 'red'))
