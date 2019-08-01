#!/usr/bin/env python3
from gatewayslib import *
from test_params import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'qa'))
from qalib import *

kmd_path = home+"/beta/komodo/src"
rpc[gateways_chain] = def_creds(gateways_chain)
rpc[prices_chain] = def_creds(prices_chain)

try:
    blocks = int(rpc['KMD'].getinfo()['blocks'])
except:
    launch_chain('KMD', [], kmd_path, kmd_pub)
    pass
try:
    blocks = int(rpc[gateways_chain].getinfo()['blocks'])
except:
    gateways_paramlist = gateways_chain_params.split(" ")
    launch_chain(gateways_chain, gateways_paramlist, kmd_path, gateways_pub)
    pass
try:
    blocks = int(rpc[prices_chain].getinfo()['blocks'])
except:
    prices_paramlist = prices_chain_params.split(" ")
    launch_chain(prices_chain, prices_paramlist, kmd_path, prices_pub)
    pass

gateway_txs = create_gateway(gateways_chain, 'KMD', 10, "Testing KMD Peg")
bind_txid = gateway_txs[0]
oracle_txid = gateway_txs[1]

spawn_oraclefeed(gateways_chain, kmd_path, oracle_txid, bind_txid)
deposit_gateway(gateways_chain, 'KMD', 1, bind_txid)