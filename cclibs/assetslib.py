#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from tokenslib import *

# DOCS: https://developers.komodoplatform.com/basic-docs/antara/antara-api/assets.html

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

def token_orders(coin, tokenid=None):
    if tokenid is None:
        orders_json = rpc[coin].tokenorders()
    else:
        orders_json = rpc[coin].tokenorders(tokenid)
    return orders_json