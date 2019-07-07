#!/usr/bin/env python3
from kmdlib import *

def token_address (chain, pubkey=None):
    rpc_connection = def_credentials(chain)
    if pubkey is None:
        result = rpc_connection.tokenaddress()
    else:
        result = rpc_connection.tokenaddress(str(pubkey))
    return result

def token_balance (chain, pubkey=None):
    rpc_connection = def_credentials(chain)
    if pubkey is None:
        result = rpc_connection.tokenbalance()
    else:
        result = rpc_connection.tokenbalance(str(pubkey))
    return result

def token_ask(chain,numtokens,tokenid,price):
    rpc_connection = def_credentials(chain)
    rawhex = rpc_connection.tokenask(numtokens,tokenid,price)
    ask_txid = rpc.connection.sendrawtransaction(rawhex['hex'])
    return ask_txid

def token_cancelask(chain,tokenid,ask_txid):
    rpc_connection = def_credentials(chain)
    rawhex = rpc_connection.tokencancelask(tokenid,ask_txid)
    ask_cancel = rpc.connection.sendrawtransaction(rawhex['hex'])
    # decode for json
    return ask_cancel

def token_fillask(chain,tokenid,ask_txid,amount):
    rpc_connection = def_credentials(chain)
    rawhex = rpc_connection.tokenfillask(tokenid,ask_txid,amount)
    ask_fill = rpc.connection.sendrawtransaction(rawhex['hex'])
    # decode for json
    return ask_fill

def token_bid(chain,numtokens,tokenid,price):
    rpc_connection = def_credentials(chain)
    rawhex = rpc_connection.tokenask(numtokens,tokenid,price)
    bid_txid = rpc.connection.sendrawtransaction(rawhex['hex'])
    return bid_txid

def token_cancelbid(chain,tokenid,bid_txid):
    rpc_connection = def_credentials(chain)
    rawhex = rpc_connection.tokencancelbid(tokenid,bid_txid)
    bid_cancel = rpc.connection.sendrawtransaction(rawhex['hex'])
    # decode for json
    return bid_cancel

def token_fillbid(chain,tokenid,bid_txid,amount):
    rpc_connection = def_credentials(chain)
    rawhex = rpc_connection.tokenfillbid(tokenid,bid_txid,amount)
    bid_fill = rpc.connection.sendrawtransaction(rawhex['hex'])
    # decode for json
    return bid_fill

def token_create(chain, tokenname, tokensupply, tokendesc):
    rpc_connection = def_credentials(chain)
    result = rpc_connection.tokencreate(str(tokenname), str(tokensupply), str(tokendesc))
    if 'hex' in result.keys():
        tokentxid = rpc_connection.sendrawtransaction(result['hex'])
        print(colorize("Tokentxid ["+str(tokentxid)+"] created", 'green'))
        return tokentxid
    else:
        print(colorize("Tokentxid creation failed: ["+str(result)+"]", 'red'))
        exit(1)

def token_info(chain,tokenid):
    rpc_connection = def_credentials(chain)
    info_json = rpc_connection.tokeninfo(tokenid)
    return info_json

def token_list(chain,tokenid):
    rpc_connection = def_credentials(chain)
    list_json = rpc_connection.tokenlist(tokenid)
    return list_json

def token_orders(chain,tokenid=None):
    rpc_connection = def_credentials(chain)
    if tokenid is None:
        orders_json = rpc_connection.tokenorders()
    else:
        orders_json = rpc_connection.tokenorders(tokenid)
    return orders_json
  
def token_transfer(chain,tokenid,dest_pubkey,amount):
    rpc_connection = def_credentials(chain)
    rawhex = rpc_connection.tokentransfer(numtokens,tokenid,price)
    bid_txid = rpc.connection.sendrawtransaction(rawhex['hex'])
    return bid_txid


def print_tokenbalance(chain, tokentxid, pubkey=""):
    rpc_connection = def_credentials(chain)
    if len(pubkey) == 66:
        result = rpc_connection.tokenbalance(str(tokentxid), str(pbkey))
    else:
        result = rpc_connection.tokenbalance(str(tokentxid))
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
