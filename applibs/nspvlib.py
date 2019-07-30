#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'qa'))
from qalib import *

supported_coins = {
                  "KMD":{"port":7777}
                  }

def nspv_broadcast(node_ip, user_pass, rawhex):
  params = {'userpass': user_pass,
            'method': 'broadcast'}
  if rawhex is not False:
    params.update({'hex':rawhex})
  r = requests.post(node_ip, json=params)
  return r

def nspv_getinfo(node_ip, user_pass, height=False):
  params = {'userpass': user_pass,
            'method': 'getinfo'}
  if height is not False:
    params.update({'height':height})
  r = requests.post(node_ip, json=params)
  print(r.json())
  return r

def nspv_getnewaddress(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'getnewaddress'}
  r = requests.post(node_ip, json=params)
  return r

def nspv_getpeerinfo(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'getpeerinfo'}
  r = requests.post(node_ip, json=params)
  return r

def nspv_hdrsproof(node_ip, user_pass, prevheight, nextheight):
  params = {'userpass': user_pass,
            'method': 'hdrsproof'}
  if prevheight is not False:
    params.update({'prevheight':prevheight})
  if nextheight is not False:
    params.update({'nextheight':nextheight})
  r = requests.post(node_ip, json=params)
  return r

def nspv_help(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'help'}
  r = requests.post(node_ip, json=params)
  return r

def nspv_listtransactions(node_ip, user_pass, address=False, isCC=False, skipcount=False, txfilter=False):
  params = {'userpass': user_pass,
            'method': 'listtransactions'}
  if address is not False:
    params.update({'address': address})
  if isCC is not False:
    params.update({'isCC': isCC})
  if skipcount is not False:
    params.update({'skipcount': skipcount})
  if txfilter is not False:
    params.update({'filter': txfilter})
  r = requests.post(node_ip, json=params)
  return r

def nspv_listunspent(node_ip, user_pass, address=False, isCC=False, skipcount=False, txfilter=False):
  params = {'userpass': user_pass,
            'method': 'listunspent'}
  if address is not False:
    params.update({'address': address})
  if isCC is not False:
    params.update({'isCC': isCC})
  if skipcount is not False:
    params.update({'skipcount': skipcount})
  if txfilter is not False:
    params.update({'filter': txfilter})
  r = requests.post(node_ip, json=params)
  return r

def nspv_login(node_ip, user_pass, wif=False):
  params = {'userpass': user_pass,
            'method': 'login'}
  if wif is not False:
    params.update({'wif': wif})
  r = requests.post(node_ip, json=params)
  print(r.json())
  return r

def nspv_logout(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'logout'}
  r = requests.post(node_ip, json=params)
  return r

def nspv_mempool(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'mempool'}
  r = requests.post(node_ip, json=params)
  return r

def nspv_notarizations(node_ip, user_pass, height):
  params = {'userpass': user_pass,
            'method': 'notarizations'}
  if height is not False:
    params.update({'height': height})
  r = requests.post(node_ip, json=params)
  return r

def nspv_spend(node_ip, user_pass, address, amount):
  params = {'userpass': user_pass,
            'method': 'spend'}
  if address is not False:
    params.update({'address': address})
  if amount is not False:
    params.update({'amount': amount})
  r = requests.post(node_ip, json=params)
  time.sleep(1)
  return r

def nspv_spentinfo(node_ip, user_pass, txid, vout):
  params = {'userpass': user_pass,
            'method': 'spend'}
  if txid is not False:
    params.update({'txid': txid})
  if vout is not False:
    params.update({'vout': vout})
  r = requests.post(node_ip, json=params)
  time.sleep(1)
  return r

def nspv_stop(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'stop'}
  r = requests.post(node_ip, json=params)
  return r

def nspv_txproof(node_ip, user_pass, txid, height):
  params = {'userpass': user_pass,
              'method': 'txproof'}
  if txid is not False:
    params.update({'txid': txid})
  if height is not False:
    params.update({'height': height})
  r = requests.post(node_ip, json=params)
  return r
