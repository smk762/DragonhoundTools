#!/usr/bin/env python3
import base58
import binascii
import hashlib
import bitcoin
from bitcoin.core import x
from bitcoin.core import CoreMainParams
from bitcoin.wallet import P2PKHBitcoinAddress
from kmdlib import *


class CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 60,
                       'SCRIPT_ADDR': 85,
                       'SECRET_KEY': 188}
bitcoin.params = CoinParams


# function to convert any address to different prefix 
# also useful for validating an address, use '3c' for prefix for validation
def addr_convert(prefix, address):
    rmd160_dict = {}
    ripemd = base58.b58decode_check(address).hex()[2:]
    net_byte = prefix + ripemd
    bina = binascii.unhexlify(net_byte)
    sha256a = hashlib.sha256(bina).hexdigest()
    binb = binascii.unhexlify(sha256a)
    sha256b = hashlib.sha256(binb).hexdigest()
    hmmmm = binascii.unhexlify(net_byte + sha256b[:8])
    final = base58.b58encode(hmmmm)
    return(final.decode())

def ntx_ranks(coin):
    score = {}
    notary_keys = {}
    print('Please wait while we calculate notarisations ...')
    info = rpc[coin].getinfo()
    height = info['blocks']
    if 'notaryname' in info:
        notaryname = info['notaryname']
    else:
        notaryname = ''

    iguana_json = rpc[coin].getiguanajson()
    for notary in iguana_json['notaries']:
        for i in notary:
            addr = str(P2PKHBitcoinAddress.from_pubkey(x(notary[i])))
            notary_keys[addr] = i

    notarysendmany = rpc[coin].getnotarysendmany()
    for block in range(2,height):
        getblock_result = rpc[coin].getblock(str(block), 2)
        if len(getblock_result['tx'][0]['vout']) > 1:
            vouts = getblock_result['tx'][0]['vout']
            for vout in vouts[1:]:
                try:
                    addr = vout['scriptPubKey']['addresses'][0]
                    if addr in notarysendmany:
                        notarysendmany[addr] += 1
                    else:
                        print('BUG in the coinbase tx, please report this.')
                except Exception as e:
                    pass

    for i in notary_keys:
        score[notary_keys[i]] = notarysendmany[i]

    total = 0
    for i in score:
        total += score[i]

    average = int((total / len(score)/4))

    s = [(k, score[k]) for k in sorted(score, key=score.get, reverse=True)]
    for k, v in s:
        if k == notaryname:
            myscore = str(k) + ' ' + str(v)
            print(colorize(myscore, 'green'))
        elif v < average:
            dropped_NN = str(k) + ' ' + str(v)
            print(colorize(dropped_NN, 'red'))
        else:
            print(k, v)

def last_ntx(coin):
    last_time = 9999999999
    txinfo = rpc[coin].listtransactions("", 77777)
    for tx in txinfo:
        if 'address' in tx:
            if tx['address'] == ntx_Radd:
                time_since = time.time() - tx['time']
                if last_time > time_since:
                    last_time = time_since
    return last_time

def sweep_funds(coin, reserve=5):
        bal = rpc[coin].getbalance()
        if bal > reserve:
            amount = bal - reserve
            rpc[coin].sendtoaddress(sweep_Radd, amount)
            print(str(amount)+" "+coin+" sent to "+sweep_Radd)

def split_funds(coin, target=100):
        utxo_count = int(unspent_count(coin)[0])
        threshold = int(target/2)
        if threshold > utxo_count:
            if coin == 'GAME' or coin == 'EMC2':
                utxosize=100000
            else:
                utxosize=10000
            split_num = target - utxo_count
            print("["+coin+"]"+" splitting "+str(split_num)+" extra UTXOs")
            params = {'agent':'iguana', 'method': 'splitfunds',
                      'coin': coin, 'duplicates': split_num,
                      'satoshis': utxosize, 'sendflag': 1 }
            r = requests.post("http://127.0.0.1:"+iguanaport, json=params)
            return r
        else:
            return "No split required"

def clean_wallet(coin, tx_max=100):
    tx_count = int(rpc[coin].getwalletinfo()['txcount'])
    print(str(tx_count)+" transactions in "+coin+" wallet")
    if tx_count > tx_max:
        try:
            print("Consolidating "+coin+ " funds")
            unconfirmed_bal = rpc[coin].getunconfirmedbalance()
            while unconfirmed_bal > 0:
                print("Waiting for unconfirmed funds ("+str(unconfirmed_bal)+") to arrive...")
                time.sleep(10)
                unconfirmed_bal = rpc[coin].getunconfirmedbalance()
            unspent = rpc[coin].listlockunspent()
            rpc[coin].lockunspent(True, unspent)
            bal = float(rpc[coin].getbalance())
            print("Consolidating "+str(bal)+" "+coin+"s to "+nn_Radd)
            txid = rpc[coin].sendtoaddress(nn_Radd, bal, "", "", True)
            wait_confirm(coin, txid)
            unconfirmed_bal = rpc[coin].getunconfirmedbalance()
            while unconfirmed_bal > 0:
                print("Waiting for unconfirmed funds ("+str(unconfirmed_bal)+") to arrive...")
                time.sleep(10)
                unconfirmed_bal = rpc[coin].getunconfirmedbalance()
            rpc[coin].cleanwallettransactions()
        except Exception as e:
            print(e)
            pass

