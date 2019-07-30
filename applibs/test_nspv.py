#!/usr/bin/env python3
from nspvlib import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'qa'))
from qalib import *
local_ip = "http://127.0.0.1:7777"

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


build_commit('nspv')
for method in nspv_methods:
  param_lists = []
  for param_list in nspv_methods[method]:
    param_lists.append(param_list)
  test_params = list(itertools.product(*param_lists))
  for x in test_params:
    print("nspv_"+method+str(x))
    if method == 'broadcast':
      resp = nspv_rpc.broadcast(userpass, *x)
    elif method == 'getnewaddress':
      resp = nspv_rpc.getnewaddress(userpass)
    elif method == 'getpeerinfo':
      resp = nspv_rpc.getpeerinfo(userpass)
    elif method == 'hdrsproof':
      resp = nspv_rpc.hdrsproof(userpass, *x)
    elif method == 'help':
      resp = nspv_rpc.help(userpass)
    elif method == 'listtransactions1':
      resp = nspv_rpc.listtransactions(userpass, *x)
    elif method == 'listtransactions2':
      resp = nspv_rpc.listtransactions(userpass, *x)
    elif method == 'listunspent1':
      resp = nspv_rpc.listunspent(userpass, *x)
    elif method == 'listunspent2':
      resp = nspv_rpc.listunspent(userpass, *x)
    elif method == 'login':
      resp = nspv_rpc.login(userpass, *x)
    elif method == 'notarizations':
      resp = nspv_rpc.notarizations(userpass, *x)
    elif method == 'spend':
      resp = nspv_rpc.spend(userpass, *x)
    elif method == 'spentinfo':
      resp = nspv_rpc.spentinfo(userpass, *x)
    elif method == 'stop':
      pass
      #resp = nspv_stop(userpass, *x)
    elif method == 'txproof':
      resp = nspv_rpc.txproof(userpass, *x)
    elif method == 'logout':
      resp = nspv_rpc.txproof(userpass)
    elif method == 'mempool':
      resp = nspv_rpc.txproof(userpass)
    try:
      print(resp)
    except Exception as e:
      print("Error: "+str(e))
      pass
    time.sleep(2)
nspv_stop(local_ip, userpass)   