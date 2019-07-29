#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *

# DOCS: https://developers.komodoplatform.com/basic-docs/antara/antara-api/tokens.html

def token_address(coin, pubkey=None):
    if pubkey is None:
        result = rpc[coin].tokenaddress()
    else:
        result = rpc[coin].tokenaddress(str(pubkey))
    return result

def token_balance(coin, pubkey=None):
    if pubkey is None:
        result = rpc[coin].tokenbalance()
    else:
        result = rpc[coin].tokenbalance(str(pubkey))
    return result

def token_ask(coin, numtokens, tokenid, price):
    rawhex = rpc[coin].tokenask(numtokens,tokenid,price)
    ask_txid = rpc[coin].sendrawtransaction(rawhex['hex'])
    return ask_txid

def token_cancelask(coin, tokenid, ask_txid):
    rawhex = rpc[coin].tokencancelask(tokenid,ask_txid)
    ask_cancel = rpc[coin].sendrawtransaction(rawhex['hex'])
    # decode for json
    return ask_cancel

def token_fillask(coin, tokenid, ask_txid, amount):
    rawhex = rpc[coin].tokenfillask(tokenid,ask_txid,amount)
    ask_fill = rpc[coin].sendrawtransaction(rawhex['hex'])
    # decode for json
    return ask_fill

def token_bid(coin, numtokens, tokenid, price):
    rawhex = rpc[coin].tokenask(numtokens,tokenid,price)
    bid_txid = rpc[coin].sendrawtransaction(rawhex['hex'])
    return bid_txid

def token_cancelbid(coin, tokenid, bid_txid):
    rawhex = rpc[coin].tokencancelbid(tokenid,bid_txid)
    bid_cancel = rpc[coin].sendrawtransaction(rawhex['hex'])
    # decode for json
    return bid_cancel

def token_fillbid(coin, tokenid, bid_txid, amount):
    rawhex = rpc[coin].tokenfillbid(tokenid,bid_txid,amount)
    bid_fill = rpc[coin].sendrawtransaction(rawhex['hex'])
    # decode for json
    return bid_fill

def token_create(coin, tokenname, tokensupply, tokendesc):
    result = rpc[coin].tokencreate(str(tokenname), str(tokensupply), str(tokendesc))
    if 'hex' in result.keys():
        tokentxid = rpc[coin].sendrawtransaction(result['hex'])
        print(colorize("Tokentxid ["+str(tokentxid)+"] created", 'green'))
        return tokentxid
    else:
        print(colorize("Tokentxid creation failed: ["+str(result)+"]", 'red'))
        exit(1)

def token_info(coin, tokenid):
    info_json = rpc[coin].tokeninfo(tokenid)
    return info_json

def token_list(coin, tokenid):
    list_json = rpc[coin].tokenlist(tokenid)
    return list_json

def token_orders(coin, tokenid=None):
    if tokenid is None:
        orders_json = rpc[coin].tokenorders()
    else:
        orders_json = rpc[coin].tokenorders(tokenid)
    return orders_json
  
def token_transfer(coin, tokenid, dest_pubkey, amount):
    rawhex = rpc[coin].tokentransfer(numtokens,tokenid,price)
    bid_txid = rpc[coin].sendrawtransaction(rawhex['hex'])
    return bid_txid


def print_tokenbalance(coin, tokentxid, pubkey=""):
    if len(pubkey) == 66:
        result = rpc[coin].tokenbalance(str(tokentxid), str(pbkey))
    else:
        result = rpc[coin].tokenbalance(str(tokentxid))
    if 'result' in result.keys():
        if result['result'] == 'success':
            tokenaddress = result['CCaddress']
            balance = result['balance']
            print(colorize("Tokentxid ["+str(tokentxid)+"] address ["+str(tokenaddress)+"] has ["+str(balance)+"] balance", 'green'))
        else:
            print(colorize("Getting token balance failed: ["+str(result)+"]", 'red'))
            exit(1)
    else:
        print(colorize("Getting token balance failed: ["+str(result)+"]", 'red'))
        exit(1)
