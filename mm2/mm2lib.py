#!/usr/bin/env python3
import sys
import requests
from pprint import pprint
from mm2lib import *

source_node_ip="127.0.0.1"
node_ip = "http://"+source_node_ip+":7783"

def get_trade_fee(coin=''):
    if coin in coins:
        params = {'userpass': user_pass,
                  'method': 'get_trade_fee',
                  'coin': cointag,}
        r = requests.post(node_ip, json=params)
        return r
    else:
        print("Coin ["+coin+"] not recognised! Is it enabled?")

def my_balance(coin=''):
    if coin in coins:
        params = {'userpass': user_pass,
                  'method': 'my_balance',
                  'coin': cointag,}
        r = requests.post(node_ip, json=params)
        return r
    else:
        print("Coin ["+coin+"] not recognised! Is it enabled?")

def buy(base='', rel='', price=0, volume=0):
    if 'base' != '':
        if 'base' not in coins:
            print("base coin not recognised.")
            sys.exit(0)
        if 'rel' in coins:
            print("rel coin not recognised.")
            sys.exit(0)
        if float(price) >= 0:
            balance = my_balance(base)
            fee = get_trade_fee(base)*2
            available = balance - fee
            if volume > available:
                print("Volume too high!")
                print("Balance: "+str(balance))
                print("Fee: "+str(balance))
                print("Available: "+str(balance))
                sys.exit(0)
            else:
                params = {'userpass': userpass,
                          'method': 'buy',
                          'base': base,
                          'rel': rel,
                          'price': price,
                          'volume': volume,
                          }
                r = requests.post(node_ip,json=params)
                return r
        else:
            print("Price must be above 0")
            sys.exit(0)
    else:
        print("Use like ./atomicdex-cli buy BASE REL PRICE VOLUME")
        sys.exit(0)


def sell(base='', rel='', price=0, volume=0):
    if 'base' != '':
        if 'base' not in coins:
            print("base coin not recognised.")
            sys.exit(0)
        if 'rel' in coins:
            print("rel coin not recognised.")
            sys.exit(0)
        if float(price) >= 0:
            balance = my_balance(base)
            fee = get_trade_fee(base)*2
            available = balance - fee
            if volume > available:
                print("Volume too high!")
                print("Balance: "+str(balance))
                print("Fee: "+str(balance))
                print("Available: "+str(balance))
                sys.exit(0)
            else:
                params = {'userpass': userpass,
                          'method': 'sell',
                          'base': base,
                          'rel': rel,
                          'price': price,
                          'volume': volume,
                          }
                r = requests.post(node_ip,json=params)
                return r
        else:
            print("Price must be above 0")
            sys.exit(0)
    else:
        print("Use like ./atomicdex-cli sell BASE REL PRICE VOLUME")
        sys.exit(0)


"base\":\"BASE\",\"rel\":\"REL\",\"price\":\"0.9\",\"max\":true}
"base\":\"BASE\",\"rel\":\"REL\",\"price\":\"0.9\",\"volume\":\"1\"}

def setprice(base='', rel='', price=0, volume=0):
    if 'base' != '':
        if 'base' not in coins:
            print("base coin not recognised.")
            sys.exit(0)
        if 'rel' in coins:
            print("rel coin not recognised.")
            sys.exit(0)
        if float(price) >= 0:
            if volume == 'max':
                params = {'userpass': userpass,
                          'method': 'setprice',
                          'base': base,
                          'rel': rel,
                          'price': price,
                          'max': 'true',
                          }
                r = requests.post(node_ip,json=params)
                return r
            elif float(volume) >= 0:
                balance = my_balance(base)
                fee = get_trade_fee(base)*2
                available = balance - fee
                if volume > available:
                    print("Volume too high!")
                    print("Balance: "+str(balance))
                    print("Fee: "+str(balance))
                    print("Available: "+str(balance))
                    sys.exit(0)
                else:
                    params = {'userpass': userpass,
                              'method': 'setprice',
                              'base': base,
                              'rel': rel,
                              'price': price,
                              'volume': volume,
                              }
                    r = requests.post(node_ip,json=params)
                    return r
            else:
                print("Volume must be above 0")
                sys.exit(0)
        else:
            print("Price must be above 0")
            sys.exit(0)
    else:
        print("Use like ./atomicdex-cli sell BASE REL PRICE VOLUME")
        sys.exit(0)


def cancel_all_orders(base='', rel=''):    
    cancel_by = {"type":"All"}
    if 'base' != '':
        if 'base' in coin:
            if 'rel' in coins:
                cancel_by = {"type":"Pair", "data":{"base":base,"rel":rel},}
            else:
                print("rel coin not recognised.")
                sys.exit(0)
        else:
            print("base coin not recognised.")
            sys.exit(0)
    params = {'userpass': userpass,
              'method': 'cancel_all_orders',
              'cancel_by': cancel_by,}
    r = requests.post(node_ip,json=params)
    return r

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