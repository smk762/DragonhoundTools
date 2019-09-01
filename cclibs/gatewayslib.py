#!/usr/bin/env python3
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from tokenslib import *
from oracleslib import *

# DOCS: https://developers.komodoplatform.com/basic-docs/antara/antara-api/gateways.html

def bind_gateway(coin, token_txid, oracle_txid, tokenname, N, M, gatewayspubkey, pubtype, p2shtype, wiftype):
    if M != 1 or N != 1:
        print(colorize("Multisig gateway not yet supported in script, using 1 of 1.", 'red'))
        M = 1
        N = 1
    tokensupply = rpc[coin].tokeninfo(token_txid)['supply']
    print("tokensupply: "+str(tokensupply))
    result = rpc[coin].gatewaysbind(token_txid, oracle_txid, tokenname, str(tokensupply), str(N), str(M), gatewayspubkey, str(pubtype), str(p2shtype), str(wiftype))
    if 'hex' in result.keys():
        bind_txid = rpc[coin].sendrawtransaction(result['hex'])
        wait_confirm(coin, bind_txid)
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
    #print("bind_gateway("+coin+", "+token_txid+", "+oracle_txid+", "+tokenname+", "+str(tokensatsupply)+", "+str(gateway_N)+", "+str(gateway_M)+", "+oraclepublisher+", 60, 85, 188)")
    bind_txid = bind_gateway(coin, token_txid, oracle_txid, tokenname, tokensatsupply, gateway_N, gateway_M, oraclepublisher, 60, 85, 188)
    return bind_txid, oracle_txid



def deposit_gateway(dest_chain, dest_addr, dest_pubkey, src_chain, src_addr,
                     gw_deposit_amount, bind_txid):
    gw_deposit_addr = rpc[dest_chain].gatewaysinfo(bind_txid)['deposit']
    print("Moving funds to KMD address...")
    self_tx = rpc[src_chain].sendtoaddress(src_addr,gw_deposit_amount*2)
    wait_confirm(src_chain,self_tx)
    print("Executing sendmany transaction")
    op_id = z_sendmany_twoaddresses(src_chain, src_addr,
                     dest_addr, 0.0001, gw_deposit_addr, gw_deposit_amount)
    time.sleep(10)
    coin_txid = opid_to_txid(src_chain, op_id)
    wait_confirm(src_chain, coin_txid)
    height = rpc[src_chain].getrawtransaction(coin_txid, 2)["height"]
    z_sendmany_hex = rpc[src_chain].getrawtransaction(coin_txid, 1)["hex"]
    claim_vout = "0"
    proof_sending_block = "[\"{}\"]".format(coin_txid)
    proof = rpc[src_chain].gettxoutproof(json.loads(proof_sending_block))
    src_info = rpc[src_chain].getinfo()
    last_ntx = src_info['notarized']
    while int(height) >= int(last_ntx):
        src_info = rpc[src_chain].getinfo()
        last_ntx = src_info['notarized']
        src_blockcount = src_info['blocks']
        print("Waiting for oraclefeed notarisation of block "+str(height))
        print("Last notarisation at block "+str(last_ntx))
        print(src_chain+" at block "+str(src_blockcount))
        time.sleep(60)
    print("Executing gateways deposit")
    deposit_hex = rpc[dest_chain].gatewaysdeposit(bind_txid, str(height), src_chain,
                                        coin_txid, claim_vout, z_sendmany_hex,
                                        proof, dest_pubkey, str(gw_deposit_amount))
    time.sleep(5)
    print(deposit_hex)
    deposit_txid = rpc[dest_chain].sendrawtransaction(deposit_hex["hex"])
    wait_confirm(dest_chain, deposit_txid)
    print(colorize("Gateways Deposit TXID ["+str(deposit_txid)+"] created", 'green'))
    return deposit_txid, coin_txid

def withdraw_gateway(coin, bind_txid, coinname, withdrawpub, amount):
    resp = rpc[coin].gatewayswithdraw(bind_txid, coinname, withdrawpub, amount)
    txid = rpc[coin].sendrawtransaction(resp['hex'])
    return txid
    
def claim_gateway(coin, bind_txid, tokenname, gateways_deposit_txid,
                  destination_pubkey, amount):
    resp = rpc[coin].gatewaysclaim(bind_txid, tokenname,
                                 gateways_deposit_txid, 
                                 destination_pubkey, str(amount))
    try:
        txid = rpc[coin].sendrawtransaction(resp['hex'])
        wait_confirm(coin, txid)
    except Exception as e:
        print("Something went wrong.")
        print(e)
        print(resp)
    return txid

