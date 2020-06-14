#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from nnlib import *

# sweep_Radd set in config.json
reserve = 5   # AMOUNT OF COINS TO KEEP IN WALLET
mining = 0
ignore = ['AXORACLE', 'ORACLEARTH', 'BTC', 'GAME', 'EMC', 'COQUICASH', 'HUSH3', 'HUSH' ]
coinlist.append('VRSC')
for coin in coinlist:
  if coin not in ignore:
    try:
      sp = split_funds(coin, 80)
      print(sp)
      dif = rpc[coin].getblockchaininfo()['difficulty']
    except:
      ressurect_chain(coin)
      pass

if coin not in ['BTC', 'EMC2', 'GIN', 'GAME', 'KMD']:
  if rpc[coin].getgenerate()['generate'] is True:
    mining += 1
    if mining > 3 or float(dif) > 2:
      rpc[coin].setgenerate(False)
      mining -= 1
  elif rpc[coin].getgenerate()['generate'] is False:
      if float(dif) < 2 and mining < 3:
          rpc[coin].setgenerate(True, 1)
          mining += 1
