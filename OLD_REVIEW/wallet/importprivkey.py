#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *

if len(sys.argv) == 2:
    if len(sys.argv[1]) == 52:
        coins = coins_info(coins_json)
        coins.append('KMD')
        rpc = {}
        for coin in coins:
            rpc[coin] = def_creds(coin)
            print(coin)
            resp = rpc[coin].importprivkey(sys.argv[1])
            print(resp)
    else:
        print("Invalid WIF")
else:
    print("Use like: ./importprivkey.py WIF")