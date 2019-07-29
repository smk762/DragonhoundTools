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

def sweep_funds(coin, reserve=25):  # A lower value may result in unmatured leftovers and lack of utxos!
    bal = int(rpc[coin].getbalance())
    if bal > reserve:
        amount = bal - reserve
        if amount > 25:
            txid = rpc[coin].sendtoaddress(sweep_Radd, amount)
            print(str(amount)+" "+coin+" sent to sweep address "+sweep_Radd+". TXID: "+txid)

def split_funds(coin, target=80):
        bal = format(rpc[coin].getbalance(), '^2.3')
        #rpc[coin].lockunspent(True, unspent)
        utxo_count = int(unspent_count(coin)[0])
        if coin == 'KMD':
            rpc[coin].setgenerate(True, 1)
            target = target*4
            threshold = int(target/8)
        else:
            threshold = int(target/6)
        split_num = target - utxo_count
        output = ' | '+'{:^9}'.format(coin)+" | " \
        +'{:^6}'.format(str(bal))+" | " \
        +'{:^9}'.format(str(utxo_count)+" utxos")+" | " \
        +'{:^10}'.format(str(target)+" target")+" | " \
        +'{:^13}'.format(str(threshold)+" threshold")+" | "
        if float(bal) > 0:
            clean_wallet(coin)
        if threshold > utxo_count:
            if coin == 'GAME' or coin == 'EMC2':
                utxosize=100000
            else:
                utxosize=10000
            params = {'agent':'iguana', 'method': 'splitfunds',
                      'coin': coin, 'duplicates': split_num,
                      'satoshis': utxosize, 'sendflag': 1 }
            r = requests.post("http://127.0.0.1:"+iguanaport, json=params)
            if r.text.find('couldnt create duplicates tx'):
                consolidate(coin)
                return output+'{:^25}'.format('Error splitting extra utxos')+' | '+str(r.json())
            else:
                return output+'{:^25}'.format('Splitting '+str(split_num)+' extra utxos')+' | '+str(r.text)
        else:
            return output+'{:^25}'.format('No split required')+' | '

def clean_wallet(coin, tx_max=120):
    tx_count = int(rpc[coin].getwalletinfo()['txcount'])
    if coin == 'KMD':
        tx_max = tx_max*2
    if tx_count > tx_max:
        try:
            consolidate(coin, 240)
        except Exception as e:
            print(e)
            pass

def format_param(param, value):
    return '-' + param + '=' + value


def get_params(coin):
    with open(home + '/komodo/src/assetchains.json') as file:
        assetchains = json.load(file)

    for chain in assetchains:
        params = []
        if chain == coin:
            for param, value in chain.items():
                if isinstance(value, list):
                    for dupe_value in value:
                        params.append(format_param(param, dupe_value))
                else:
                    params.append(format_param(param, value))
#            return(' '.join(params))
            return params

def move_chain(coin):
    print("tryna move "+coin)
    rpc[coin].setgenerate(True, 1)
    block_count = rpc[coin].getblockcount()
    next_block = block_count + 1
    consolidate(coin)
    while next_block > block_count:
        time.sleep(60)
        block_count = rpc[coin].getblockcount()
    rpc[coin].setgenerate(False)

def reindex_chain(coin):
    rpc[coin].stop()
    time.sleep(30)
    params = get_params(coin)
    Popen(["komodod", '-ac_name='+coin, '-reindex', "-pubkey="+pubkey]+params)

def consolidate(coin, tx_delay=900):    
    last_tx = rpc[coin].listtransactions("", 1)[0]['timereceived']
    now = time.time()
    if int(now) > int(last_tx)+tx_delay:
        bal = float(rpc[coin].getbalance())
        if bal > 0:
            unspent = rpc[coin].listlockunspent()
            rpc[coin].lockunspent(True, unspent)
            print("Consolidating "+str(bal)+" "+coin+"s to "+nn_Radd)
            txid = rpc[coin].sendtoaddress(nn_Radd, bal, "", "", True)
            wait_confirm(coin, txid)
            time.sleep(30)
            rpc[coin].cleanwallettransactions()


def refresh_wallet():
    print("pending")
    pass
    # importprivkey <privkey> "" false