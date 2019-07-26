#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
from os.path import expanduser

# Get and set config
cwd = os.getcwd()
home = expanduser("~")
port = 7771
local_ip = "http://127.0.0.1:"+str(port)
userpass = "userpass"

supported_coins = {
                  "KMD":{"port":7771}
                  }
nspv_methods = ['broadcast', 'getnewaddress', 'getpeerinfo', 'hdrsproof', 'help',
                'listtransactions', 'listunspent', 'login', 'logout', 'mempool',
                'notarizations', 'spend'. 'spentinfo', 'stop', 'txproof']

def nspv_broadcast(node_ip, user_pass, rawhex):
  params = {'userpass': user_pass,
            'method': 'broadcast',
            'hex':rawhex}
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
  return r


def nspv_getinfo(node_ip, user_pass, height=False):
  params = {'userpass': user_pass,
            'method': 'getinfo'}
  if height is not False:
    params.update({'height':height})
  r = requests.post(node_ip, json=params)
  print(r.json())
  time.sleep(0.5)
  return r

def nspv_getnewaddress(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'getnewaddress'}
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
  return r

def nspv_getpeerinfo(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'getpeerinfo'}
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
  return r

def nspv_hdrsproof(node_ip, user_pass, prevheight, nextheight):
  params = {'userpass': user_pass,
            'prevheight': prevheight,
            'nextheight': nextheight,
            'method': 'hdrsproof',
            }
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
  return r

def nspv_help(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'help'}
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
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
  time.sleep(0.5)
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
  time.sleep(0.5)
  return r

def nspv_login(node_ip, user_pass, wif):
  params = {'userpass': user_pass,
            'method': 'login',
            'wif':wif}
  r = requests.post(node_ip, json=params)
  print(r.json())
  time.sleep(0.5)
  return r

def nspv_logout(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'logout'}
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
  return r

def nspv_mempool(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'mempool'}
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
  return r

def nspv_notarizations(node_ip, user_pass, height):
  params = {'userpass': user_pass,
            'method': 'notarizations',
            'height': height}
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
  return r

def nspv_spend(node_ip, user_pass, address, amount):
  params = {'userpass': user_pass,
            'method': 'spend',
            'address': address,
            'amount': float(amount) }
  r = requests.post(node_ip, json=params)
  time.sleep(1)
  return r

def nspv_spentinfo(node_ip, user_pass, txid, vout):
  params = {'userpass': user_pass,
            'method': 'spend',
            'txid': txid,
            'vout': vout }
  r = requests.post(node_ip, json=params)
  time.sleep(1)
  return r

def nspv_stop(node_ip, user_pass):
  params = {'userpass': user_pass,
            'method': 'stop'}
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
  return r

def nspv_txproof(node_ip, user_pass):
  params = {'userpass': user_pass,
              'method': 'txproof',
              'txid': txid,
              'height': height}
  r = requests.post(node_ip, json=params)
  time.sleep(0.5)
  return r
