#!/usr/bin/env python3
import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'qa'))
from qalib import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from tokenslib import *
from gatewayslib import *
from oracleslib import *

# DOCS: https://github.com/Mixa84/komodo/wiki/Pegs-CC

def setup_pegs_chain(chain_name, paramlist, kmd_path):
    spawn_2chainz(chain_name, paramlist, kmd_path)
    

def setup_pegs_gateway(src_chain, dest_chain, tokensupply):
    token_supply = 1000
    token_name = src_chain+"T"
    token_desc = "Pegged "+src_chain+" Token"
    token_txid = token_create(src_chain, token_name, token_supply, tokendesc)
    wait_confirm(src_chain, token_txid)

def setup_pegs_account(src_chain, source_addr,
                       dest_chain, dest_addr, dest_pubkey,
                       gateways_amount, bind_txid,
                       pegs_txid, debt_ratio_pct=60):
    source_balance = rpc[src_chain].getbalance()
    if source_balance < float(gateways_amount):
        print(src_chain+" balance is too low! Send some to "+src_chain)
    gateways_info = rpc[dest_chain].gatewaysinfo(bind_txid)
    gateways_addr = gateways_info['deposit']
    token_txid = gateways_info['tokenid']
    op_id = rpc[src_chain].z_sendmany(source_addr, [{"address":dest_addr,"amount":0.0001},{"address":gateways_addr,"amount":gateways_amount}])
    op_status = rpc[src_chain].z_getoperationstatus([op_id])
    print()
    while op_status[0]['status'] != 'success':
        if 'error' in op_status[0]:
            print(op_status[0]['error'])
            if op_status[0]['error']['message'] == 'Could not find any non-coinbase UTXOs to spend.':
                print("You need to send some "+src_chain+" to "+source_addr)
                print(rpc[src_chain].listaddressgroupings())
                sys.exit(0)

        else:
            print("waiting for z_sendmany to complete")
        op_status = rpc[src_chain].z_getoperationstatus([op_id])
        time.sleep(10)
    coin_txid = op_status[0]['result']['txid']
    wait_confirm(src_chain, coin_txid)
    print("Coin TXID: "+coin_txid)
    tx_info = rpc[src_chain].gettransaction(coin_txid)
    print(tx_info)
    for account in tx_info['details']:
        if account['address'] == dest_addr:
            claim_vout = account['vout']
    deposit_hex = tx_info['hex']
    blockheight = rpc[src_chain].getblock(tx_info['blockhash'])['height']

    proof = rpc[src_chain].gettxoutproof([coin_txid])
    print(bind_txid)
    print("Blockheight: "+str(blockheight))
    print(src_chain)
    print(coin_txid)
    print(str(claim_vout))
    #print(deposit_hex)
    #print(proof)
    print(dest_pubkey)
    print(str(gateways_amount))
    resp = rpc[dest_chain].gatewaysdeposit(bind_txid, str(blockheight), src_chain,
                                     coin_txid, str(claim_vout),
                                     deposit_hex, proof,
                                     dest_pubkey, str(gateways_amount))
    while resp['result'] == 'error':
        print(resp['error'])
        print("waiting for notarisation")
        time.sleep(20)
        resp = rpc[dest_chain].gatewaysdeposit(bind_txid, str(blockheight), src_chain,
                                     coin_txid, str(claim_vout),
                                     deposit_hex, proof,
                                     dest_pubkey, str(gateways_amount))
        
    gw_deposit_txid = rpc[dest_chain].sendrawtransaction(resp['hex'])
    wait_confirm(dest_chain, gw_deposit_txid)
    resp = rpc[dest_chain].gatewaysclaim(bind_txid, coin,
                                 gateways_deposit_txid, 
                                 destination_pubkey, str(amount))
    gw_claim_txid = rpc[dest_chain].sendrawtransaction(resp['hex'])
    wait_confirm(dest_chain, gw_claim_txid)
    resp = rpc[dest_chain].pegsfund(pegs_txid, token_txid, str(gateways_amount))
    pegs_fund_txid = rpc[dest_chain].sendrawtransaction(pegs_fund_resp['hex'])
    print("Coin TXID: "+coin_txid)
    print("Gateways Deposit TXID: "+gw_deposit_txid)
    print("Gateways Claim TXID: "+gw_claim_txid)
    print("Pegs Fund TXID: "+pegs_fund_txid)

def set_pegs_debt_ratio(pegs_txid, target_debt_ratio=60):
    pegs_info = rpc[dest_chain].pegsinfo(pegs_txid)
    pegs_accounthistory = rpc[dest_chain].pegsinfo(pegs_txid)

    pegs_amount = gateways_amount * debt_ratio_pct/100 
    pegs_get_resp = rpc[dest_chain].pegsget(pegs_txid, token_txid, pegs_amount)
    pegs_get_txid = rpc[dest_chain].sendrawtransaction(pegs_get_resp['hex'])

    pegs_redeem_resp = rpc[dest_chain].pegsredeem(pegs_txid, token_txid)
    pegs_redeem_txid = rpc[dest_chain].sendrawtransaction(pegs_redeem_resp['hex'])

def liquidate_worst_account(pegs_txid, token_txid):
    pegs_worstaccounts = rpc[dest_chain].pegsworstaccounts(pegs_txid)
    if pegs_worstaccounts['result'] == 'success':
        acct_txid = pegs_worstaccounts['KMD']
    pegs_liquidate = rpc[dest_chain].pegsliquidate(pegs_txid, token_txid, acct_txid)

def unallocated():
    pegs_exchange_resp = rpc[dest_chain].pegsexchange(pegs_txid, token_txid, gateways_amount)
    txid = rpc[dest_chain].sendrawtransaction(pegs_exchange_resp['hex'])

    pegs_redeem = rpc[dest_chain].pegsredeem(pegs_txid, token_txid)

def test_pegs_rpcs():
    KMD_token_txid = "babf52d3f8586393a3ca45e07ccd9ab247fd56c5104bef3aa6a83be3f104831a"
    Oracle_txid = "bde7c4fb8f7f402891d350715c308179193e4c961c90cac0740a7e89d561b437"
    Gateway_txid = "e41b98f104d5d3a8f94742f5b0237a9efdd6999bea4af2ce64228c7280167b40"
    Pegs_txid = "a130861d422655cb28ffbf788c3b4a07748ba67eb7c413c9440b7cbbfcb9d296"
    pegs_info = rpc[dest_chain].pegsinfo(pegs_txid)
    print(pegs_info)