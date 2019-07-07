#!/usr/bin/env python3
from kmdlib import *

def bind_gateway(chain, tokentxid, oracletxid, tokenname, tokensupply, N, M, gatewayspubkey, pubtype, p2shtype, wiftype):
    rpc_connection = def_credentials(chain)
    if M != str(1) or N != str(1):
        print(colorize("Multisig gateway not yet supported in script, using 1 of 1.", 'red'))
        M = 1
        N = 1
    result = rpc_connection.gatewaysbind(tokentxid, oracletxid, tokenname, str(tokensupply), str(N), str(M), gatewayspubkey, str(pubtype), str(p2shtype), str(wiftype))
    if 'hex' in result.keys():
        bindtxid = rpc_connection.sendrawtransaction(result['hex'])
        print(colorize("Bindtxid ["+str(bindtxid)+"] created", 'green'))
        return bindtxid
    else:
        print(colorize("Bindtxid creation failed: ["+str(result)+"]", 'red'))
        exit(1)

def create_gateway():    
    chain = user_input('Enter asset-chain to create tokens on: ', str)
    tokenname = user_input('Enter token name: ', str)
    tokendesc = user_input('Enter token description: ', str)
    tokensupply = user_input('Enter token supply: ', str)
    tokentxid = create_tokens(chain, tokenname, tokendesc, tokensupply)
    oracletxid = create_oracle(chain, tokenname, 'blockheaders', 'Ihh')
    datafee = user_input('Enter oracle data fee (in satoshis): ', str)
    while int(datafee) < 10000:
        print(colorize("Datafee too low, set to 10k or more", 'blue'))
        datafee = user_input('Enter oracle data fee (in satoshis): ', str)
    oraclepublisher = register_oracle(chain, oracletxid, datafee)
    funds = user_input('Enter amount of funds to send to oracle: ', str)
    fund_oracle(chain, oracletxid, oraclepublisher, funds)
    N = user_input('Enter total number of gateways signatures: ', str)
    M = user_input('Enter number gateways signatures required to withdraw: ', str)
    tokensatsupply = 100000000*int(tokensupply)
bindtx = bind_gateway(chain, tokentxid, oracletxid, tokenname, tokensatsupply, N, M, oraclepublisher, 60, 85, 188)