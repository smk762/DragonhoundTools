#!/usr/bin/env python3
import sys
import requests
from pprint import pprint
from mm2lib import *

# TODO: move this to config.json
source_ip="127.0.0.1"
external_ip="116.203.120.163"
mm2_port = "7783"
this_node = "http://"+source_ip+":"+mm2_port
external_node = "http://"+external_ip+":"+mm2_port

def get_trade_fee(coin='', node_ip='http://127.0.0.1:7783'):
    if coin in coins:
        params = {'userpass': user_pass,
                  'method': 'get_trade_fee',
                  'coin': coin,}
        r = requests.post(node_ip, json=params)
        return r
    else:
        print("Coin ["+coin+"] not recognised! Is it enabled?")

def my_balance(coin='', node_ip='http://127.0.0.1:7783'):
    if coin in coins:
        params = {'userpass': user_pass,
                  'method': 'my_balance',
                  'coin': coin,}
        r = requests.post(node_ip, json=params)
        return r
    else:
        print("Coin ["+coin+"] not recognised! Is it enabled?")

def buy(base='', rel='', price=0, volume=0, node_ip='http://127.0.0.1:7783'):
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


def sell(base='', rel='', price=0, volume=0, node_ip='http://127.0.0.1:7783'):
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

def setprice(base='', rel='', price=0, volume=0, node_ip='http://127.0.0.1:7783'):
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

def cancel_order(uuid='', node_ip='http://127.0.0.1:7783'):
    if uuid == '':
        print("Use like ./atomicdex-cli cancel_order UUID")
        sys.exit(0)
    else:
        params = {'userpass': userpass,
          'method': 'cancel_order',
          'uuid': uuid,}
    r = requests.post(node_ip,json=params)
    return r

def coins_needed_for_kick_start(node_ip='http://127.0.0.1:7783'):
    params = {'userpass': userpass,
              'method': 'coins_needed_for_kick_start',}
    r = requests.post(node_ip,json=params)
    return r

def electrum(node_ip='http://127.0.0.1:7783'):
    pass

def enable(node_ip='http://127.0.0.1:7783'):
    pass

def get_enabled_coins(node_ip='http://127.0.0.1:7783'):
    pass

def atomicdex_help(node_ip='http://127.0.0.1:7783'):
    pass

def my_orders(node_ip='http://127.0.0.1:7783'):
    pass

def my_recent_swaps(node_ip='http://127.0.0.1:7783'):
    pass

def my_swap_status(node_ip='http://127.0.0.1:7783'):
    pass

def my_tx_history(node_ip='http://127.0.0.1:7783'):
    pass

def order_status(node_ip='http://127.0.0.1:7783'):
    pass

def orderbook(node_ip='http://127.0.0.1:7783'):
    pass

def send_raw_transaction(node_ip='http://127.0.0.1:7783'):
    pass

def stop(node_ip='http://127.0.0.1:7783'):
    params = {'method': 'stop',}
    r = requests.post(node_ip,json=params)
    return r

def withdraw(coin, address, amount, node_ip='http://127.0.0.1:7783'):
    params = {'userpass': userpass,
              'method': 'withdraw',
              'coin': cointag,
              'to':address,
              'amount':amount,}
    pass

def cancel_all_orders(base='', rel='', node_ip='http://127.0.0.1:7783'):
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