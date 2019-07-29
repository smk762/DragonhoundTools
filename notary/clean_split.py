#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from nnlib import *

# sweep_Radd set in config.json
reserve = 5   # AMOUNT OF COINS TO KEEP IN WALLET
mining = 0
ignore = ['AXORACLE', 'ORACLEARTH', 'BTC', 'GAME', 'EMC', 'COQUICASH' ]
for coin in coinlist:
  try:
    if coin not in ignore:
       cl = clean_wallet(coin)
       sw = sweep_funds(coin, 25)
  except:
    pass
  sp = split_funds(coin, 80)
  print(sp)
  dif = rpc[coin].getblockchaininfo()['difficulty']

if coin not in ['BTC', 'EMC2', 'GIN', 'GAME', 'KMD']:
  if rpc[coin].getgenerate()['generate'] is True:
    mining += 1
    if mining > 6 or float(dif) > 2:
      rpc[coin].setgenerate(False)
      mining -= 1
  elif rpc[coin].getgenerate()['generate'] is False:
      if float(dif) < 2 and mining < 6:
          rpc[coin].setgenerate(True, 1)
          mining += 1