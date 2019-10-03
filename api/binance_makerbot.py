#!/usr/bin/env python3
import os
from os.path import expanduser
import sys
import binance_api
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'applibs'))
import mm2lib

home = expanduser("~")
mm2_path = home+'/pytomicDEX'

try:
	mm2lib.my_balance('http://127.0.0.1:7783', 'user_pass', 'KMD')
except:
	os.chdir(mm2_path)
	mm2lib.start_mm2()

	pass
mm2lib.activate_all('http://127.0.0.1:7783', 'user_pass', mm2lib.coins)
mm2lib.my_balances('http://127.0.0.1:7783', 'user_pass', mm2lib.coins)
print(binance_api.get_price('KMDBTC'))