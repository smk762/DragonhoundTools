#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
for coin in coinlist:
    print(coin+": "+str(rpc[coin].getbalance()))