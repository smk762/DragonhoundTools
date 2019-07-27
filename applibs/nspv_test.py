#!/usr/bin/env python3
import itertools
from nspvlib import *

# params list format [no value (false), good value, bad value]
wif = [False, 'UrJUbSqsb1chYxmQvScdnNhVc2tEJEBDUPMcxCCtgoUYuvyvLKvB', 'thiswontwork']
height = [False, 777, 'notnum']
prevheight = [False, 765, 'notnum']
nextheight = [False, 785, 'notnum']
address = [False, 'RYPzyuLXdT9JYn7pemYaX3ytsY3btyaATY', 'not_an_addr']
isCCno = [False, 0, 'notnum']
isCCyes = [False, 1, 'notnum']
skipcount = [False, 2, 'notnum']
txfilter = ['not implemented yet']
amount = [False, 2, 'notnum']
txid = [False, 'f261773a389445100d8dfe4fc0b2d9daeaf90ef6264435e739fbd698624b77d6', 'not_txid']
vout = [False, 1,'d']
rawhex = [False, '', 'nothex']

nspv_methods = {'broadcast':[rawhex],
                'getnewaddress':[],
                'getpeerinfo':[],
                'hdrsproof':[prevheight,nextheight],
                'help':[],
                'listtransactions1':[address,isCCno,skipcount],
                'listtransactions2':[address,isCCyes,skipcount],
                'listunspent1':[address,isCCno,skipcount],
                'listunspent2':[address,isCCyes,skipcount],
                'login':[wif], 'logout':[], 'mempool':[],
                'notarizations':[height],
                'spend':[address,amount],
                'spentinfo':[txid,vout],
                'txproof':[txid,height],
                'stop':[]}
for method in nspv_methods:
  param_lists = []
  for param_list in nspv_methods[method]:
    param_lists.append(param_list)
  test_params = list(itertools.product(*param_lists))
  for x in test_params:
    print("nspv_"+method+str(x))
    if method == 'broadcast':
      resp = nspv_broadcast(local_ip, userpass, *x).json()
    elif method == 'getnewaddress':
      resp = nspv_getnewaddress(local_ip, userpass, *x).json()
    elif method == 'getpeerinfo':
      resp = nspv_getpeerinfo(local_ip, userpass, *x).json()
    elif method == 'hdrsproof':
      resp = nspv_hdrsproof(local_ip, userpass, *x).json()
    elif method == 'help':
      resp = nspv_help(local_ip, userpass, *x).json()
    elif method == 'listtransactions1':
      resp = nspv_listtransactions(local_ip, userpass, *x).json()
    elif method == 'listtransactions2':
      resp = nspv_listtransactions(local_ip, userpass, *x).json()
    elif method == 'listunspent1':
      resp = nspv_listunspent(local_ip, userpass, *x).json()
    elif method == 'listunspent2':
      resp = nspv_listunspent(local_ip, userpass, *x).json()
    elif method == 'login':
      resp = nspv_login(local_ip, userpass, *x).json()
    elif method == 'notarizations':
      resp = nspv_notarizations(local_ip, userpass, *x).json()
    elif method == 'spend':
      resp = nspv_spend(local_ip, userpass, *x).json()
    elif method == 'spentinfo':
      resp = nspv_spentinfo(local_ip, userpass, *x).json()
    elif method == 'stop':
      resp = nspv_stop(local_ip, userpass, *x).json()
    elif method == 'txproof':
      resp = nspv_txproof(local_ip, userpass, *x).json()
    print(resp)
    time.sleep(2)
