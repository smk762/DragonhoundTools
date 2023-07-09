#!/usr/bin/env python3
import requests
import socket
import json
import time
import hashlib
import codecs
import base58
import logging
import logging.handlers
from logging import Handler, Formatter
import bitcoin
from bitcoin.core import x
from bitcoin.core import CoreMainParams
from bitcoin.wallet import P2PKHBitcoinAddress

# TODO: Refactor, use latest class libs (electrum & insight)

SEASON = "Season_5"

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%d-%b-%y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class KMD_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 60,
                       'SCRIPT_ADDR': 85,
                       'SECRET_KEY': 188}

class SFUSD_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 63,
                       'SCRIPT_ADDR': 85,
                       'SECRET_KEY': 188}

class PBC_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 60,
                       'SCRIPT_ADDR': 85,
                       'SECRET_KEY': 188}

class BTC_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 0,
                       'SCRIPT_ADDR': 5,
                       'SECRET_KEY': 128}

class LTC_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 48,
                       'SCRIPT_ADDR': 5,
                       'SECRET_KEY': 176}

class AYA_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 23,
                       'SCRIPT_ADDR': 5,
                       'SECRET_KEY': 176}

class EMC2_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 33,
                       'SCRIPT_ADDR': 5,
                       'SECRET_KEY': 176}

class GAME_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 38,
                       'SCRIPT_ADDR': 5,
                       'SECRET_KEY': 166}

class GIN_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 38,
                       'SCRIPT_ADDR': 10,
                       'SECRET_KEY': 198}

class GLEEC_3P_CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 35,
                       'SCRIPT_ADDR': 38,
                       'SECRET_KEY': 65}

# Update this if new third party coins added
coin_params = {
    "KMD": KMD_CoinParams,
    "BTC": BTC_CoinParams,
    "LTC": LTC_CoinParams,
    "PBC": PBC_CoinParams,
    "SFUSD": SFUSD_CoinParams,
    "AYA": AYA_CoinParams,
    "EMC2": EMC2_CoinParams,
    "GAME": GAME_CoinParams,
    "GIN": GIN_CoinParams,
    "GLEEC_AC": KMD_CoinParams,
    "GLEEC_3P": GLEEC_3P_CoinParams

}

# Get 3rd party / main dPoW coins

#r = requests.get("http://stats.kmd.io/api/info/coins/?dpow_active=1")
#r = requests.get("http://116.203.120.91:8762/api/info/coins")
#dpow_coins = r.json()['results'][0]

def get_mainnet_chains(coins_data):
    main_chains = []
    for coin in coins_data:
        if coins_data[coin]['dpow']['server'].lower() == "dpow-mainnet":
            main_chains.append(coin)
    if "GLEEC" in main_chains:
        main_chains.remove("GLEEC")
    main_chains.append("GLEEC_AC")
    return main_chains

def get_third_party_chains(coins_data):
    third_chains = []
    for coin in coins_data:
        if coins_data[coin]['dpow']['server'].lower() == "dpow-3p":
            third_chains.append(coin)
    if "GLEEC" in third_chains:
        third_chains.remove("GLEEC")
    third_chains.append("GLEEC_3P")
    return third_chains

main_coins = requests.get(f"http://stats.kmd.io/api/info/dpow_server_coins/?season={SEASON}&server=Main").json()['results']
third_party_coins = requests.get(f"http://stats.kmd.io/api/info/dpow_server_coins/?season={SEASON}&server=Third_Party").json()['results']

print(main_coins)
print(third_party_coins)

# third party coins with same base58 params as KMD
antara_coins = main_coins[:]+['CHIPS', 'MCL', 'VRSC', 'GLEEC_AC']
if 'LTC' in antara_coins:
    antara_coins.remove('BTC')

main_coins = main_coins[:]+['LTC']
third_party_coins = third_party_coins[:]+['KMD']
all_coins = third_party_coins[:]+main_coins

main_coins.sort()
third_party_coins.sort()
antara_coins.sort()
all_coins.sort()

if 'TOKEL' not in antara_coins:
    antara_coins.append('TOKEL')

if 'TOKEL' not in third_party_coins:
    third_party_coins.append('TOKEL')

for coin in antara_coins:
    coin_params.update({coin:KMD_CoinParams})

electrums = {}
electrum_info = requests.get("http://stats.kmd.io/api/info/electrums").json()['results']

for coin in electrum_info:
    if len(electrum_info[coin]) > 0:
        electrum = electrum_info[coin][0].split(":")
        electrums.update({
            coin:{
                "url":electrum[0],
                "port":electrum[1]
                }
            })

def get_from_electrum(url, port, method, params=[]):
    params = [params] if type(params) is not list else params
    socket.setdefaulttimeout(15)
    s = socket.create_connection((url, port))

    s.send(json.dumps({"id": 0, "method": 'server.version', "params": ['nn_balance_scan','1.4']}).encode() + b'\n')
    #print(json.loads(s.recv(99999)[:-1].decode()))
    s.send(json.dumps({"id": 0, "method": method, "params": params}).encode() + b'\n')
    time.sleep(15)
    return json.loads(s.recv(99999)[:-1].decode().split('\n')[-1])


def lil_endian(hex_str):
    return ''.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)][::-1])

def get_addr_from_pubkey(pubkey, coin):
    bitcoin.params = coin_params[coin]
    return str(P2PKHBitcoinAddress.from_pubkey(x(pubkey)))

def get_p2pk_scripthash_from_pubkey(pubkey):
    scriptpubkey = '21' +pubkey+ 'ac'
    scripthex = codecs.decode(scriptpubkey, 'hex')
    s = hashlib.new('sha256', scripthex).digest()
    sha256_scripthash = codecs.encode(s, 'hex').decode("utf-8")
    script_hash = lil_endian(sha256_scripthash)
    return script_hash

def get_p2pkh_scripthash_from_pubkey(pubkey):
    publickey = codecs.decode(pubkey, 'hex')
    s = hashlib.new('sha256', publickey).digest()
    r = hashlib.new('ripemd160', s).digest()
    scriptpubkey = "76a914"+codecs.encode(r, 'hex').decode("utf-8")+"88ac"
    h = codecs.decode(scriptpubkey, 'hex')
    s = hashlib.new('sha256', h).digest()
    sha256_scripthash = codecs.encode(s, 'hex').decode("utf-8")
    script_hash = lil_endian(sha256_scripthash)
    return script_hash

def get_full_electrum_balance(pubkey, url, port):
    p2pk_scripthash = get_p2pk_scripthash_from_pubkey(pubkey)
    p2pkh_scripthash = get_p2pkh_scripthash_from_pubkey(pubkey)
    p2pk_resp = get_from_electrum(url, port, 'blockchain.scripthash.get_balance', p2pk_scripthash)
    logger.info(p2pk_resp)
    p2pkh_resp = get_from_electrum(url, port, 'blockchain.scripthash.get_balance', p2pkh_scripthash)
    logger.info(p2pkh_resp)
    p2pk_confirmed_balance = p2pk_resp['result']['confirmed']
    p2pkh_confirmed_balance = p2pkh_resp['result']['confirmed']
    p2pk_unconfirmed_balance = p2pk_resp['result']['unconfirmed']
    p2pkh_unconfirmed_balance = p2pkh_resp['result']['unconfirmed']
    total_confirmed = p2pk_confirmed_balance + p2pkh_confirmed_balance
    total_unconfirmed = p2pk_unconfirmed_balance + p2pkh_unconfirmed_balance
    total = total_confirmed + total_unconfirmed
    return total/100000000

def get_dexstats_balance(chain, addr):
    if chain == "MIL":
        url = 'http://mil.kmdexplorer.io/api/addr/'+addr
    else:
        url = 'http://'+chain.lower()+'.explorer.dexstats.info/insight-api-komodo/addr/'+addr
    r = requests.get(url)
    balance = r.json()['balance']
    return balance


def get_balance(chain, addr, pubkey, url="", port="", notary=""):

    balance = -1
    try:
        if chain in electrums:
            try:

                if not url:
                    url = electrums[chain]["url"]
                if not port:
                    port = electrums[chain]["port"]
                source = url+":"+str(port)
                balance = get_full_electrum_balance(pubkey, url, port)
            except Exception as e:
                print("!!!!! "+chain+" "+source+" ERR: "+str(e))
                balance = -1
                try:
                    source = "dexstats"
                    balance = get_dexstats_balance(chain, addr)
                except Exception as e:
                    print("!!!!! "+chain+" "+source+" ERR: "+str(e))
                    balance = -1

        elif chain == "AYA":
            url = 'https://ayaexplorer.guarda.co/api/address/'+addr
            r = requests.get(url)
            try:
                source = 'ayaexplorer.guarda.co'
                balance = r.json()['balance']
            except Exception as e:
                print("!!!!! "+chain+" "+source+" ERR: "+str(e))
                balance = -1

        else:
            try:
                source = "dexstats"
                balance = get_dexstats_balance(chain, addr)
            except Exception as e:
                print("!!!!! "+chain+" "+source+" ERR: "+str(e))
                balance = -1
        print(f"chain: {chain}")
        print(f"source: {source}")
        print(f"addr: {addr}")
        print(f"balance: {balance}")
        print(f"notary: {notary}")


    except Exception as e:
        print("!!!!! get_balance ERR: "+str(e))
        balance = -1
    if balance != -1:
        print(f">> chain: {chain}")
        print(f">> source: {source}")
        print(f">> addr: {addr}")
        print(f">> balance: {balance}")
        print(f">> notary: {notary}")
        print("<<<<< "+'{:^12}'.format(chain)+" | "+'{:^40}'.format(source)+ f"|   OK   | {addr} | {balance} | {notary}")
    else:
        source = "NO SRC"
        print("##### "+'{:^12}'.format(chain)+" | "+'{:^40}'.format(source)+ f"| FAILED | {addr} | {balance} | {notary}")
    return balance, source
