#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'qa'))
from qalib import *


# TODO: move this to config.json
source_ip="127.0.0.1"
external_ip="116.203.120.163"
mm2_port = "7783"
this_node = "http://"+source_ip+":"+mm2_port
external_node = "http://"+external_ip+":"+mm2_port


def get_cointag(method):
    try:
        cointag = sys.argv[2]
        return cointag
    except:
        print("No coin parameter! Use './atomicDEX-cli "+method+" COIN'")
        sys.exit(0)

def get_uuid(method):
    try:
        uuid = sys.argv[2]
        return uuid
    except:
        print("No UUID parameter! Use './atomicDEX-cli "+method+" COIN'")
        sys.exit(0)

def get_baserel(method):  
    try:
        base = sys.argv[2]
        rel = sys.argv[3]
        return base,rel
    except:
        print("Base / Rel parameter not specified! Use './atomicDEX-cli "+method+" BASE REL'")
        sys.exit(0)
        
def get_sendparams(method):  
    try:
        cointag = sys.argv[2]
        addr = sys.argv[3]
        amount = sys.argv[4]
        return cointag,addr,amount
    except:
        print("Parameters not specified! Use './atomicDEX-cli "+method+" COIN ADDRESS AMOUNT'")
        sys.exit(0)

def get_tradeparams(method):  
    try:
        base = sys.argv[2]
        rel = sys.argv[3]
        vol = sys.argv[4]
        price = sys.argv[5]
        return base, rel, vol, price
    except:
        print("Parameters not specified! Use './atomicDEX-cli "+method+" BASE REL BASEVOLUME RELPRICE'")
        sys.exit(0)

#TODO: change this to match python methods
def help_mm2(node_ip, user_pass):
    params = {'userpass': user_pass, 'method': 'help'}
    r = requests.post(node_ip, json=params)
    return r

## MM2 management
def start_mm2(logfile):
  mm2_output = open(logfile,'w+')
  Popen(["./mm2"], stdout=mm2_output, stderr=mm2_output, universal_newlines=True)
  print("Marketmaker 2 started. Use 'tail -f "+logfile+"' for mm2 console messages")

def stop_mm2(node_ip, user_pass):
    params = {'userpass': user_pass, 'method': 'stop'}
    r = requests.post(node_ip, json=params)
    return r

def enable(node_ip, user_pass, cointag, tx_history=True):
    for coin in coins:
        if coin['tag'] == cointag:
            params = {'userpass': user_pass,
                      'method': 'enable',
                      'coin': cointag,
                      'mm2':1,  
                      'tx_history':tx_history,}
            r = requests.post(node_ip, json=params)
            return r

def electrum(node_ip, user_pass, cointag, tx_history=True):
    for coin in coins:
        if coin['tag'] == cointag:
            if 'contract' in coin:
                params = {'userpass': user_pass,
                          'method': 'enable',
                          'urls':coin['electrum'],
                          'coin': cointag,
                          'swap_contract_address': coin['contract'],
                          'mm2':1,
                          'tx_history':tx_history,}
            else:
                params = {'userpass': user_pass,
                          'method': 'electrum',
                          'servers':coin['electrum'],
                          'coin': cointag,
                          'mm2':1,
                          'tx_history':tx_history,}
            r = requests.post(node_ip, json=params)
            return r

def activate(node_ip, user_pass, cointag):
  for coin in coins:
    if coin['tag'] == cointag:
      if coin['activate_with'] == 'native':
        r = enable(node_ip, user_pass, coin['tag'])
        print("Activating "+coin['tag']+" in native mode")
        return r
      else:
        r = electrum(node_ip, user_pass, coin['tag'])
        print("Activating "+coin['tag']+" with electrum")
        return r
  print("Coin not in mm2coins.py!")
  print("Available coins:")
  print(str(cointags))
  sys.exit(0)

def my_balance(node_ip, user_pass, cointag):
    params = {'userpass': user_pass,
              'method': 'my_balance',
              'coin': cointag,}
    r = requests.post(node_ip, json=params)
    return r

def orderbook(node_ip, user_pass, base, rel):
    params = {'userpass': user_pass,
              'method': 'orderbook',
              'base': base, 'rel': rel,}
    r = requests.post(node_ip, json=params)
    return r

def my_orders(node_ip, user_pass):
    params = {'userpass': user_pass, 'method': 'my_orders',}
    r = requests.post(node_ip, json=params)
    return r

def cancel_all(node_ip, user_pass):
    params = {'userpass': user_pass,
              'method': 'cancel_all_orders',
              'cancel_by': {"type":"All"},}
    r = requests.post(node_ip,json=params)
    return r

def cancel_pair(node_ip, user_pass, base, rel):
    params = {'userpass': user_pass,
              'method': 'cancel_all_orders',
              'cancel_by': {
                    "type":"Pair",
                    "data":{"base":base,"rel":rel},
                    },}
    r = requests.post(node_ip,json=params)
    return r

### Order Placement

def setprice(node_ip, user_pass, base, rel, basevolume, relprice, trademax=False, cancel_previous=True):
    params = {'userpass': user_pass,
              'method': 'setprice',
              'base': base,
              'rel': rel,
              'volume': basevolume,
              'price': relprice,
              'max':trademax,
              'cancel_previous':cancel_previous,}
    r = requests.post(node_ip, json=params)
    return r

def buy(node_ip, user_pass, base, rel, basevolume, relprice):
    params ={'userpass': user_pass,
             'method': 'buy',
             'base': base,
             'rel': rel,
             'volume': basevolume,
             'price': relprice,}
    r = requests.post(node_ip,json=params)
    return r

def sell(node_ip, user_pass, base, rel, basevolume, relprice):
    params = {'userpass': user_pass,
              'method': 'sell',
              'base': base,
              'rel': rel,
              'volume': basevolume,
              'price': relprice,}
    r = requests.post(node_ip,json=params)
    return r


def withdraw(node_ip, user_pass, cointag, address, amount, max_amount=False):
    params = {'userpass': user_pass,
              'method': 'withdraw',
              'coin': cointag,
              'to': address,
              'amount': amount,
              'max': max_amount,}
    r = requests.post(node_ip, json=params)
    return r 

def send_raw_transaction(node_ip, user_pass, cointag, rawhex):
    params = {'userpass': user_pass,
              'method': 'send_raw_transaction',
              'coin': cointag, "tx_hex":rawhex,}
    r = requests.post(node_ip, json=params)
    return r


def my_tx_history(node_ip, user_pass, cointag, limit=10, from_id=''):
    if from_id == '':
        params ={'userpass': user_pass,
                 'method': 'my_tx_history',
                 'coin': cointag,
                 'limit': limit,}
    else:
        params = {'userpass': user_pass,
                  'method': 'my_tx_history',
                  'coin': cointag,
                  'limit': limit,
                  'from_id':from_id,}        
    r = requests.post(node_ip, json=params)
    return r


def order_status(node_ip, user_pass, order_uuid):
    params = {'userpass': user_pass,
              'method': 'order_status',
              'uuid': order_uuid,}
    r = requests.post(node_ip,json=params)
    return r

def cancel_order(node_ip, user_pass, order_uuid):
    params = {'userpass': user_pass,
              'method': 'cancel_order',
              'uuid': order_uuid,}
    r = requests.post(node_ip,json=params)
    return r

#need to use the uuid from taker on both maker/taker
def my_swap_status(node_ip, user_pass, swap_uuid):
    params = {'userpass': user_pass,
              'method': 'my_swap_status',
              'params': {"uuid": swap_uuid},}
    r = requests.post(node_ip,json=params)
    return r

def my_recent_swaps(node_ip, user_pass, from_uuid='', limit=10):
    if from_uuid=='':
        params = {'userpass': user_pass,
                  'method': 'my_recent_swaps',
                  'limit': int(limit),}
        
    else:
        params = {'userpass': user_pass,
                  'method': 'my_recent_swaps',
                  "limit": int(limit),
                  "from_uuid":from_uuid,}
    r = requests.post(node_ip,json=params)
    return r

### Looping on all activated. Not yet in ./atomicDEX-cli methods list
def electrums(node_ip, user_pass, coins):
    for coin in coins:
        activation_response = electrum(node_ip, user_pass, coin['tag'])
        print(activation_response)    
    
def activate_all(node_ip, user_pass, coins):
  for coin in coins:
    if coin['activate_with'] == 'native':
      r = enable(node_ip, user_pass, coin['tag'])
      print("Activating "+coin['tag']+" in native mode")
    else:
      r = electrum(node_ip, user_pass, coin['tag'])
      print("Activating "+coin['tag']+" with electrum")
    print(r.json())
    

def my_balances(node_ip, user_pass, coins):
    api_coins = {"BTC":"bitcoin","BCH":"bitcoin-cash","DGB":"digibyte","DASH":"dash",
                "QTUM":"qtum","DOGE":"dogecoin","KMD":"komodo",
                "ETH":"ethereum", "BAT":"basic-attention-token",
                "USDC":"usd-coin", "LTC":"litecoin", "VRSC":"verus-coin"}
    url = 'https://api.coingecko.com/api/v3/simple/price'
    coin_string = ",".join(list(api_coins.values()))
    params = dict(ids=coin_string,vs_currencies='usd')
    r = requests.get(url=url, params=params)
    prices = r
    total = 0
    for coin in coins:
        try:
            balance_response = my_balance(node_ip, user_pass, coin['tag'])
            address = balance_response["address"]
            balance = balance_response["balance"]
            coin = balance_response["coin"]
            if coin in api_coins:
                price = prices[api_coins[coin]]['usd']
                value = round(float(balance)*float(price),2)
                total += value
                print(address+" : "+str(balance)+" "+coin+" (USD$"+str(value)+")")
            else:
                print(address+" : "+str(balance)+" "+coin)
        except Exception as e:
            print(e)
            pass
    print("TOTAL BALANCE: USD$"+str(total))

def orderbooks(node_ip, user_pass, coins):
    for base in coins:
        for rel in coins:
            if base != rel:
                try:
                    orderbook_response = orderbook(node_ip, user_pass, base['tag'], rel['tag']).json()
                    print(orderbook_response)
                    if len(orderbook_response['bids']) > 0 or len(orderbook_response['asks']) > 0:
                        print(orderbook_response)
                        #for bid in orderbook_response['bids']:
                        #    print("Base: "+orderbook_response['base']+", Rel: "+orderbook_response['rel'])
                        #    print(str(bid['maxvolume'])+" at "+str(bid['price']))
                except Exception as e:
                    print("Orderbooks error: "+str(e))
                    sys.exit(0)
