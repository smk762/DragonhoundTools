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
    #print("gatewaysbind tokentxid oracletxid tokenname tokensupply N M gatewayspubkey pubtype p2shtype wiftype")
    #print("gatewaysbind "+tokentxid+" "+oracletxid+" "+tokenname+" "+str(tokensupply)+" "+str(N)+" "+str(M)+" "+gatewayspubkey+" "+str(pubtype)+" "+str(p2shtype)+" "+str(wiftype))
    result = rpc[coin].gatewaysbind(tokentxid, oracletxid, tokenname, str(tokensupply), str(N), str(M), gatewayspubkey, str(pubtype), str(p2shtype), str(wiftype))
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



def deposit_gateway(dest_chain, dest_addr, dest_pubkey, src_chain, src_addr, token_name, gw_deposit_amount, bind_txid):
    gw_deposit_addr = rpc[dest_chain].gatewaysinfo(bind_txid)['deposit']
    print(colorize("Gateways Deposit Address ["+str(gw_deposit_addr)+"] created", 'green'))
    print(colorize("Dest Pubkey ["+str(dest_pubkey)+"]", 'green'))
    txid = rpc[src_chain].sendtoaddress(src_addr, float(gw_deposit_amount*2))
    wait_confirm(src_chain, txid)
    op_id = rpc[src_chain].z_sendmany(src_addr, [{"address":dest_addr, "amount":0.0001},{"address":gw_deposit_addr, "amount":gw_deposit_amount}])
    print('~/Mixa84/komodo/src/komodo-cli z_sendmany '+src_addr+'[{"address":"'+dest_addr+', "amount":0.0001 },{"address":"'+gw_deposit_addr+'", "amount":'+str(gw_deposit_amount)+'}]')
    op_status = rpc[src_chain].z_getoperationstatus([op_id])
    while op_status[0]['status'] != 'success':
        print(op_status)
        time.sleep(15)
        op_status = rpc[src_chain].z_getoperationstatus([op_id])
    coin_txid = op_status[0]['result']['txid']
    print(colorize("Coin TXID ["+str(bind_txid)+"]", 'green'))
    wait_confirm(src_chain, coin_txid)
    tx_info = rpc[src_chain].getrawtransaction(coin_txid, 2)
    # print(tx_info)
    #for account in tx_info['details']:
     #   if account['address'] == dest_addr:
      #      claim_vout = account['vout']
    claim_vout = 0
    deposit_hex = tx_info['hex']
    height = tx_info['height']
    proof_sending_block = "[\"{}\"]".format(coin_txid)
    proof = rpc[src_chain].gettxoutproof(json.loads(proof_sending_block))
    #print("~/Mixa84/komodo/src/komodo-cli -ac_name="+dest_chain \
#        +" gatewaysdeposit "+bind_txid+" "+str(height)+" "+ src_chain \
 #               +" "+coin_txid+" "+str(claim_vout)+" "+deposit_hex, proof \
  #              +" "+dest_pubkey+" "+str(gw_deposit_amount))
    wait_notarised(src_chain, txid)
    print("Waiting for z_sendmany notarisation...")
    resp = rpc[dest_chain].gatewaysdeposit(bind_txid, str(height), src_chain,
                                     coin_txid, str(claim_vout),
                                     deposit_hex, proof,
                                     dest_pubkey, str(gw_deposit_amount))
    while resp['result'] == 'error':
        print(resp['error'])
        if resp['error'] == "deposittxid didnt validate":
            print("Something went wrong, exiting...")
 #           print("deposit_hex: "+deposit_hex)
  #          print("proof: "+proof)
            print("op_id: "+op_id)
    #        print("coin_txid: "+coin_txid)
            sys.exit(0)
        src_blockcount = rpc[src_chain].getblockcount()
        print("waiting for notarisation. "+src_chain+" at block "+str(src_blockcount))
        time.sleep(60)
        resp = rpc[dest_chain].gatewaysdeposit(bind_txid, str(height), src_chain,
                                     coin_txid, str(claim_vout),
                                     deposit_hex, proof,
                                     dest_pubkey, str(gw_deposit_amount))
    gw_deposit_txid = rpc[dest_chain].sendrawtransaction(resp['hex'])
    wait_confirm(dest_chain, gw_deposit_txid)
    print(colorize("Gateways Deposit TXID ["+str(gw_deposit_txid)+"] created", 'green'))
    return gw_deposit_txid, coin_txid

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

