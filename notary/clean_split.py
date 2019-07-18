#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from nnlib import *

# sweep_Radd set in config.json
reserve = 5   # AMOUNT OF COINS TO KEEP IN WALLET

ignore = ['AXORACLE', 'ORACLEARTH', 'BTC', 'GAME', 'EMC' ]
for coin in coinlist:
  try:
    if coin not in ignore:
        clean_wallet(coin)
    bal = int(rpc[coin].getbalance())
    if bal > 20:
      amount = bal - reserve
      rpc[coin].sendtoaddress(sweep_Radd, str(amount))
      print(str(amount)+" "+coin+" sent to sweep address "+sweep_Radd)
  except:
    pass
  r = split_funds(coin, 100)
  try:
    if 'error' in r.json():
  	  print(r.json()['error'])
  except:
    print(r)
