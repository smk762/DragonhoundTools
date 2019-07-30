#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *

# DOCS: https://developers.komodoplatform.com/basic-docs/antara/antara-api/tokens.html

# params list format [no value (false), good value, bad value]
pubkey = [False, '03e2619d87be65ea2488ad4ad2658853b06cf4a400ca1cb039e65b73709cd3b634', 'not_pubkey']
tokenid = [False, 'validtokeidhere', 'invalid_tokenID']
name = [False, 'token_name', 999]
supply = [False, 7777, 'notnum']
description = [False, 'token_description', 999]
destpubkey = [False, '03e2619d87be65ea2488ad4ad2658853b06cf4a400ca1cb039e65b73709cd3b634', 'not_pubkey']
amount = [False, 7, 'notnum']

tokens_methods = {'tokenaddress':[pubkey],
                'tokenbalance':[tokenid, pubkey],
                'tokencreate':[name, supply, description],
                'tokeninfo':[tokenid],
                'tokenlist':[],
                'tokentransfer':[tokenid,destpubkey,amount]}

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
