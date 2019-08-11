#!/usr/bin/env python3
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from tokenslib import *
from oracleslib import *

# DOCS: https://developers.komodoplatform.com/basic-docs/antara/antara-api/gateways.html

def bind_gateway(coin, tokentxid, oracletxid, tokenname, tokensupply, N, M, gatewayspubkey, pubtype, p2shtype, wiftype):
    if M != 1 or N != 1:
        print(colorize("Multisig gateway not yet supported in script, using 1 of 1.", 'red'))
        M = 1
        N = 1
    result = rpc[coin].gatewaysbind(tokentxid, oracletxid, tokenname, str(tokensupply), str(N), str(M), gatewayspubkey, str(pubtype), str(p2shtype), str(wiftype))
    if 'hex' in result.keys():
        bind_txid = rpc[coin].sendrawtransaction(result['hex'])
        print(colorize("Bindtxid ["+str(bind_txid)+"] created", 'green'))
        return bind_txid
    else:
        print(colorize("Bindtxid creation failed: ["+str(result)+"]", 'red'))
        exit(1)

def create_gateway(coin, tokenname, tokensupply, tokendesc):
    token_txid = token_create(coin, tokenname, tokensupply, tokendesc)
    oracle_txid = create_oracle(coin, tokenname, 'blockheaders', 'Ihh')
    oraclepublisher = rpc[coin].getinfo()['pubkey']
    gateway_N = 1
    gateway_M = 1
    tokensatsupply = 100000000*int(tokensupply)
    print("bind_gateway("+coin+", "+token_txid+", "+oracle_txid+", "+tokenname+", "+str(tokensatsupply)+", "+str(gateway_N)+", "+str(gateway_M)+", "+oraclepublisher+", 60, 85, 188"))
    bind_txid = bind_gateway(coin, token_txid, oracle_txid, tokenname, tokensatsupply, gateway_N, gateway_M, oraclepublisher, 60, 85, 188)
    return bind_txid, oracle_txid

def spawn_oraclefeed(coin, komodo_path, oracle_txid, bind_txid):
    oraclefeed_log = cwd+"/oraclefeed.log"
    oraclefeed_output = open(oraclefeed_log,'w+')
    os.chdir(komodo_path)
    build_proc = subprocess.run(['gcc', 'cc/dapps/oraclefeed.c' '-lm' '-o' 'oraclefeed'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    print(build_proc.stdout)
    pubkey = rpc[coin].getinfo()['pubkey']
    subprocess.Popen([komodo_path+'/oraclefeed', coin, oracle_txid, pubkey, 'Ihh', bind_txid], stdout=oraclefeed_output, stderr=oraclefeed_output, universal_newlines=True)
    print("Build complete, oraclefeed started.")
    print(" Use tail -f "+test_log+" for "+app+" console messages")


def deposit_gateway(token, asset_name, gw_deposit_amount, bind_txid):
    gw_deposit_addr = rpc[token].gatewaysinfo(bind_txid)['deposit']
    token_addr = rpc[token].getnewaddress()
    token_pubkey = rpc[token].validateaddress(token_addr)['pubkey']
    asset_addr = rpc[asset_name].getnewaddress()
    txid = rpc[asset_name].sendtoadress(asset_addr, float(gw_deposit_amount*2))
    wait_confirm(asset_name, txid)
    op_id = rpc[asset_name].z_sendmany(asset_addr, [{"address":token_addr, "amount":0.0001},{"address":gw_deposit_addr, "amount":gw_deposit_amount}])
    op_status = rpc[asset_name].z_getoperationstatus([op_id])
    while op_status['status'] != 'success':
        print(op_status)
        time.sleep(15)
        op_status = rpc[asset_name].z_getoperationstatus([op_id])
    coin_txid = op_status['txid']
    tx_info = rpc[asset_name].gettransaction(coin_txid)
    deposithex = tx_info['hex']
    tx_blockhash = tx_info['blockhash']
    height = rpc[asset_name].getblock(tx_blockhash)['height']
    proof = rpc[asset_name].gettxoutproof(coin_txid)
    claim_vout = 0
    resp = rpc[coin].gatewaysdeposit(bind_txid, height, asset_name,
                                     coin_txid, claim_vout,
                                     deposithex, proof,
                                     token_pubkey, gw_deposit_amount)
    txid = rpc[coin].sendrawtransaction(resp['hex'])
    return txid

def withdraw_gateway(coin, bind_txid, coinname, withdrawpub, amount):
    resp = rpc[coin].gatewayswithdraw(bind_txid, coinname, withdrawpub, amount)
    txid = rpc[coin].sendrawtransaction(resp['hex'])
    return txid
    
def claim_gateway(bind_txid, coin, gateways_deposit_txid,
                  destination_pubkey, amount):
    resp = pegsRPC.gatewaysclaim(bind_txid, coin,
                                 gateways_deposit_txid, 
                                 destination_pubkey, amount)
    txid = pegsRPC.sendrawtransaction(resp['hex'])
    return txid

