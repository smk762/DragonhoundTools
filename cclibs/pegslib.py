#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cc'))
from tokenslib import *
from oracleslib import *


# DOCS: https://github.com/Mixa84/komodo/wiki/Pegs-CC

def create_gateway(coin, tokenname, tokendesc, tokensupply):
    tokentxid = token_create(coin, tokenname, tokensupply, tokendesc)
    oracletxid = create_oracle(coin, tokenname, 'blockheaders', 'Ihh')
    oraclepublisher = rpc[coin].getinfo()['pubkey']
    gateway_N = 1
    gateway_M = 2
    tokensatsupply = 100000000*int(tokensupply)
    bind_txid = bind_gateway(coin, tokentxid, oracletxid, tokenname, tokensatsupply, gateway_N, gateway_M, oraclepublisher, 60, 85, 188)
    return bind_txid