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
        sweep_funds(coin, 5)
  except:
    pass
  r = split_funds(coin, 100)
  try:
    if 'error' in r.json():
  	  print(r.json()['error'])
  except:
    print(r)
