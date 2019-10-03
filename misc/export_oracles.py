#!/usr/bin/env python3
import os
import re
import sys
import json
import http
import time
import codecs
import requests
import platform
from slickrpc import Proxy
from os.path import expanduser
 
# Get and set config
cwd = os.getcwd()
home = expanduser("~")
rpc = {}

ac_dir = home+"/.komodo"

def colorize(string, color):
    colors = {
            'black':'\033[30m',
            'red':'\033[31m',
            'green':'\033[32m',
            'orange':'\033[33m',
            'blue':'\033[34m',
            'purple':'\033[35m',
            'cyan':'\033[36m',
            'lightgrey':'\033[37m',
            'darkgrey':'\033[90m',
            'lightred':'\033[91m',
            'lightgreen':'\033[92m',
            'yellow':'\033[93m',
            'lightblue':'\033[94m',
            'pink':'\033[95m',
            'lightcyan':'\033[96m',
    }
    if color not in colors:
        return str(string)
    else:
        return colors[color] + str(string) + '\033[0m'

def select_ac(interrogative):
    while True:
        dir_list = next(os.walk(home+"/.komodo"))[1]
        ac_list = []
        row = ''
        i = 1
        for folder in dir_list:
            if folder not in ['notarisations', 'blocks', 'database', 'chainstate']:
                ac_list.append(folder)
                if i < 10:
                    row += " ["+str(i)+"] "+'{:<14}'.format(folder)
                else:
                    row += "["+str(i)+"] "+'{:<14}'.format(folder)
                if len(row) > 64:
                    print(row)
                    row = ''
                i += 1
        selection = validate_selection(interrogative, ac_list)
        return selection

def validate_selection(interrogative, selection_list):
    while True:
        index = int(input(colorize(interrogative, 'orange')))-1
        try:
            selected = selection_list[index]
            return selected
        except:
            print(colorize("Invalid selection, must be number between 1 and "+str(len(selection_list)), 'red'))
            pass

def def_creds(chain):
    rpcport =''
    coin_config_file = ''
    if chain == 'KMD':
        coin_config_file = str(ac_dir + '/komodo.conf')
    elif chain == 'BTC':
        coin_config_file = str(home + '/.bitcoin/bitcoin.conf')
    if coin_config_file == '':
        coin_config_file = str(ac_dir + '/' + chain + '/' + chain + '.conf')                
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
        elif chain == 'KMD':
            rpcport = 8333
        else:
            print("rpcport not in conf file, exiting")
            print("check "+coin_config_file)
            exit(1)
    return(Proxy("http://%s:%s@127.0.0.1:%d"%(rpcuser, rpcpassword, int(rpcport))))

def wait_confirm(coin, txid):
    start_time = time.time()
    mempool = rpc[coin].getrawmempool()
    while txid in mempool:
        print(colorize("Waiting for "+txid+" confirmation...",'orange'))
        time.sleep(60)
        mempool = rpc[coin].getrawmempool()
        #print(mempool)
        looptime = time.time() - start_time
        if looptime > 900:
            print(colorize("Transaction timed out",'red'))
            return False
    print(colorize("Transaction "+txid+" confirmed!",'green'))
    return True

def create_oracle(coin, oracle_name, oracle_description, oracletype):
    print(colorize("Creating "+oracle_name+" oracle",'blue'))
    rpc[coin] = def_creds(coin)
    result = rpc[coin].oraclescreate(oracle_name, oracle_description, oracletype)
    oracleResult=result['result']
    while oracleResult != 'success':
        print(result)
        result = rpc[coin].oraclescreate(oracle_name, oracle_description, oracletype)
        oracleResult=result['result']
        time.sleep(30)
    oracleHex=result['hex']
    oracle_txid = rpc[coin].sendrawtransaction(oracleHex)
    wait_confirm(coin, oracle_txid)
    print(colorize(oracle_name+" created!",'green'))
    oraclesList = str(rpc[coin].oracleslist())
    loop = 0
    while oraclesList.find(oracle_txid) < 0:
        loop += 1
        time.sleep(30)
        oraclesList = str(rpc[coin].oracleslist())
        print(colorize("Waiting for oracle "+oracle_name+" to list, "+str(30*loop)+" sec", 'orange'))
        if loop > 30:
            print(colorize("Oracle ["+oracle_txid+"] didnt list, exiting.",'red'))
            sys.exit(0)
    print(colorize("Oracle  "+oracle_name+"  listing confirmed",'green'))
    fund_oracle(coin, oracle_txid)
    register_oracle(coin, oracle_txid)
    subscribe_oracle(coin, oracle_txid, 10000)
    return oracle_txid

def fund_oracle(coin, oracle_txid):
    print(colorize("Funding ["+oracle_txid+"] oracle", 'blue'))
    rpc[coin] = def_creds(coin)
    fund = rpc[coin].oraclesfund(oracle_txid)
    oracleResult=fund['result']
    while oracleResult != 'success':
        fund = rpc[coin].oraclesfund(oracle_txid)
        oracleResult=fund['result']
    oracleHex=fund['hex']
    fund_txid = rpc[coin].sendrawtransaction(oracleHex)
    wait_confirm(coin, fund_txid)
    print(colorize("["+oracle_txid+"] funded",'green'))
    time.sleep(5)

def subscribe_oracle(coin, oracle_txid, total_amount):
    print(colorize("Subscribing ["+oracle_txid+"] oracle", 'blue'))
    publisher = rpc[coin].getinfo()['pubkey']
    rpc[coin] = def_creds(coin)
    amount = float(total_amount)/100
    sub_list = []
    for i in range (1,101):
        result = rpc[coin].oraclessubscribe(oracle_txid, publisher, str(amount))
        orcl_hex = result['hex']
        sub_txid = rpc[coin].sendrawtransaction(orcl_hex)
        time.sleep(1)
        sub_list.append(sub_txid)
    pending_subs = len(rpc[coin].getrawmempool())
    while pending_subs > 0:
        print(colorize("Waiting for "+str(pending_subs)+" subscriptions to confirm", 'orange'))
        time.sleep(30)
        pending_subs = len(rpc[coin].getrawmempool())
    print(colorize("["+oracle_txid+"] subscribed!",'green'))

def register_oracle(coin, oracle_txid, datafee=0.001):
    print(colorize("Registering ["+oracle_txid+"] oracle", 'blue'))
    rpc[coin] = def_creds(coin)
    fund_oracle(coin, oracle_txid)
    rego = rpc[coin].oraclesregister(oracle_txid, str(datafee))
    time.sleep(15)
    oracleResult=rego['result']
    while oracleResult != 'success':
        print('ORACLE REGISTRATION ERROR:' + oracleResult)
        if oracleResult.find('oraclesfund') != -1:
            fund_oracle(coin, oracle_txid)
        time.sleep(15)
        rego = rpc[coin].oraclesregister(oracle_txid, str(datafee))
        oracleResult=rego['result']
    oracleHex=rego['hex']
    rego_txid = rpc[coin].sendrawtransaction(oracleHex)
    wait_confirm(coin, rego_txid)
    print(colorize("["+oracle_txid+"] registered",'green'))

def check_rego(coin, oracle_txid):
    print(colorize("Checking registration for ["+oracle_txid+"] oracle", 'blue'))
    rpc[coin] = def_creds(coin)
    publishers = []
    pubkey = rpc[coin].getinfo()['pubkey']
    oracle_info = rpc[coin].oraclesinfo(oracle_txid)
    if len(oracle_info['registered']) > 0:
        for pub in oracle_info['registered']:
            publishers.append(pub['publisher'])
        if pubkey not in publishers:
            register_oracle(coin, oracle_txid)
    else:
        register_oracle(coin, oracle_txid)

def check_funds(coin, oracle_txid):
    print(colorize("Checking funds for ["+oracle_txid+"] oracle", 'blue'))
    rpc[coin] = def_creds(coin)
    publishers = []
    pubkey = rpc[coin].getinfo()['pubkey']
    oracle_info = rpc[coin].oraclesinfo(oracle_txid)
    for pub in oracle_info['registered']:
        if pubkey == pub['publisher']:
            funds = pub['funds']
    if float(funds) < 1000:
        subscribe_oracle(coin, oracle_txid, 1000)

def write2oracle(coin, oracle_txid, message):
    rpc[coin] = def_creds(coin)
    check_rego(coin, oracle_txid)
    check_funds(coin, oracle_txid)
    print(colorize("Writing to ["+oracle_txid+"] oracle", 'blue'))
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
    oraclesdata_result = rpc[coin].oraclesdata(oracle_txid, fullhex)
    result = oraclesdata_result['result']
    i = 0
    while result == 'error':
        print('ORACLE WRITE ERROR: '+ oraclesdata_result['error'])
        if oraclesdata_result['error'].find('oraclesfund') != -1:
            fund_oracle(coin, oracle_txid)
        if oraclesdata_result['error'].find('illegal') != -1:
            return ''
        time.sleep(30)
        oraclesdata_result = rpc[coin].oraclesdata(oracle_txid, fullhex)
        result = oraclesdata_result['result']
        i += 1
        if i > 10:
            print(colorize("Message ["+message+"] failed to be written to oracle.", 'red'))
            return False
    rawtx = oraclesdata_result['hex']
    sendrawtransaction_result = rpc[coin].sendrawtransaction(rawtx)
    print(colorize("Message ["+message+"] written to oracle.", 'green'))
    return sendrawtransaction_result

def export_oracles(source_chain):
    print(colorize("Exporting "+str(source_chain)+" oracles", 'blue'))
    oracles_archive = []
    rpc[source_chain] = def_creds(source_chain)
    oracles_list = rpc[source_chain].oracleslist()
    for oracle_txid in oracles_list:
        oracle_samples = []
        oracle_data = {}
        oracle_info = rpc[source_chain].oraclesinfo(oracle_txid)
        reg_json=oracle_info['registered']
        for reg_pub in reg_json:
            if 'baton' in reg_pub:
                baton = reg_pub['baton']
                samples = rpc[source_chain].oraclessamples(oracle_txid, baton, str(100))
                oracle_data.update({"name":oracle_info['name']})
                oracle_data.update({"description":oracle_info['description']})
                oracle_data.update({"format":oracle_info['format']})
                if samples is not None:
                    for sample in samples['samples']:
                        oracle_samples.append(sample['data'][0])
                oracle_data.update({"data":oracle_samples})
                if oracle_info['name'].find("Spamtest") == -1 and oracle_info['name'].find("_recreated") == -1:
                    print(colorize(oracle_info['name']+" oracle records retrieved.", 'green'))
                    oracles_archive.append(oracle_data)
            else:
                print(colorize("EXPORT ERROR: Oracle baton does not exist.", 'red'))
    return oracles_archive

def import_oracles(dest_chain, oracles_archive):
    rpc[dest_chain] = def_creds(dest_chain)
    i = 1
    for entry in oracles_archive:
        print(colorize("Importing oracle "+str(i)+"/"+str(len(oracles_archive))+" oracles", 'blue'))
        if entry['name'].find("Spamtest") == -1 and entry['name'].find("_recreated") == -1:
            oracle_name = entry['name']
            oracles_list = rpc[dest_chain].oracleslist()
            created = False
            for txid in oracles_list:
                if oracle_name == rpc[dest_chain].oraclesinfo(txid)['name']:
                    created = True
            if created is False:
                oracle_txid = create_oracle(dest_chain, oracle_name, entry['description'], entry['format'])
                j = 1
                num_msg = len(entry['data'])
                for msg in entry['data']:
                    write2oracle(dest_chain, oracle_txid, msg)
                    print(colorize(str(j)+" of "+str(num_msg)+" messages on "+oracle_name+" imported...", 'orange'))
                    time.sleep(10)
                    j += 1
            else:
                print(colorize("Oracle ["+entry['name']+"] already created", 'blue'))
                j = 1
                num_msg = len(entry['data'])
                for msg in entry['data']:
                    write2oracle(dest_chain, txid, msg)
                    print(colorize(str(j)+" of "+str(num_msg)+" messages on "+oracle_name+" imported...", 'orange'))
                    time.sleep(10)
                    j += 1
        i += 1

export_chain = select_ac("Select Smartchain to export from: ")
import_chain = select_ac("Select Smartchain to import to: ")
oracles_archive = export_oracles(export_chain)
import_oracles(import_chain, oracles_archive)