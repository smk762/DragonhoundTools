#!/usr/bin/env python3
import sys
import requests
from pprint import pprint
from mm2lib import *

node_ip = "http://"+source_node_ip+":7783"
try:
    method = sys.argv[1]
except:
    print("No method parameter! Use `./atomicDEX-cli help` to view available commands")
    method = ''
    r = mm2_method(node_ip, userpass, 'help')
    print(r.text)
    sys.exit(0)
noparam_methods = ["my_orders",
                   "help",
                   "stop",
                   "coins_needed_for_kick_start",
                   "my_recent_swaps"]
cointag_methods = [ 'withdraw', 'my_balance']

if method in noparam_methods:
    r = mm2_method(node_ip, userpass, method)
elif method == 'cancel_all_orders':
    if len(sys.argv) < 3:
        cancel_by = {"type":"All"}
    elif len(sys.argv) == 4:
        base = sys.argv[2]
        rel = sys.argv[3]
        cancel_by = {"type":"Pair", "data":{"base":base,"rel":rel},}
    else:
        print("Use like ./atomicdex-cli cancel_all_orders BASE REL")
        sys.exit(0)
    params = {'userpass': userpass,
              'method': 'cancel_all_orders',
              'cancel_by': cancel_by,}
    r = requests.post(node_ip,json=params)
elif method == 'withdraw':
    if len(sys.argv) == 5:
        cointag = sys.argv[2]
        address = sys.argv[3]
        amount = sys.argv[4]
        params = {'userpass': userpass,
                  'method': 'withdraw',
                  'coin': cointag,
                  'to':address,
                  'amount':amount,}
    else:
        print("Use like ./atomicdex-cli withdraw COIN ADDRESS AMOUNT")
        sys.exit(0)
    r = requests.post(node_ip, json=params)
elif method == 'my_balance':
    if len(sys.argv) == 3:
        cointag = sys.argv[2]
        r = my_balance(node_ip, userpass, cointag)
    else:
        r = ''
        print("Use like ./atomicdex-cli my_balance COIN")
        sys.exit(0)
elif method == 'calcaddress':
    if len(sys.argv) == 4:
        passphrase = sys.argv[2]
        cointag = sys.argv[3]
        r = calcaddress(node_ip, userpass, passphrase, cointag)
    else:
        r = ''
        print('Use like ./atomicdex-cli calcaddress "passphrase" COIN')
        sys.exit(0)
elif method == 'my_swap_status':
    if len(sys.argv) == 3:
        uuid = sys.argv[2]
        r = my_swap_status(node_ip, userpass, uuid)
    else:
        r = ''
        print("Use like ./atomicdex-cli my_swap_status UUID")
        sys.exit(0)



else:
    print("Method not recognised! Is it listed below?")
    r = mm2_method(node_ip, userpass, 'help')
    sys.exit(0)
try:
    pprint(r.json(), indent=1)
except:
print(r.text)