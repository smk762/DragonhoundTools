#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from tokenslib import *
from gatewayslib import *
from oracleslib import *

# DOCS: https://github.com/Mixa84/komodo/wiki/Pegs-CC

def setup_pegs_account(source_chain, source_addr,
					   dest_chain, dest_addr, dest_pubkey,
					   gateways_addr, gateways_amount, 
					   bind_txid, pegs_txid, token_txid, debt_ratio_pct=60
					   ):

	sendmany_params = []
	sendmany_params.append({"address":dest_addr,"amount":0.0001})
	sendmany_params.append({"address":gateways_addr,"amount":gateways_amount})
	op_id = rpc[source_chain].z_sendmany(source_addr, sendmany_params)
	op_status = rpc[source_chain].z_getoperationstatus([op_id])
	while op_status['success'] ! = success:
		op_status = rpc[source_chain].z_getoperationstatus([op_id])
		time.sleep(10)
	coin_txid = op_status['result']['txid']
	tx_info = rpc[source_chain].gettransaction(coin_txid)
	for account in tx_info['details']:
		if account['address'] == dest_addr:
			claim_vout = account['vout']
	deposit_hex = tx_info['hex']
	blockheight = rpc[source_chain].getblock(tx_info['blockhash'])
	proof = rpc[source_chain].gettxoutproof(coin_txid)
	resp = rpc[dest_chain].gatewaysdeposit(bind_txid, blockheight, source_chain,
                                     coin_txid, claim_vout,
                                     deposit_hex, proof,
                                     dest_pubkey, gateways_amount)
    gw_deposit_txid = rpc[dest_chain].sendrawtransaction(resp['hex'])

    resp = rpc[dest_chain].gatewaysclaim(bind_txid, coin,
                                 gateways_deposit_txid, 
                                 destination_pubkey, amount)
    gw_claim_txid = rpc[dest_chain].sendrawtransaction(resp['hex'])

	resp = rpc[dest_chain].pegsfund(pegs_txid, token_txid, gateways_amount)
	pegs_fund_txid = rpc[dest_chain].sendrawtransaction(pegs_fund_resp['hex'])

def set_pegs_debt_ratio(pegs_txid, target_debt_ratio=60):
	pegs_info = rpc[dest_chain].pegsinfo(pegs_txid)
	pegs_accounthistory = rpc[dest_chain].pegsinfo(pegs_txid)


	pegs_amount = gateways_amount * debt_ratio_pct/100 
	pegs_get_resp = rpc[dest_chain].pegsget(pegs_txid, token_txid, pegs_amount)
	pegs_get_txid = rpc[dest_chain].sendrawtransaction(pegs_get_resp['hex'])

	pegs_redeem_resp = rpc[dest_chain].pegsredeem(pegs_txid, token_txid)
	pegs_redeem_txid = rpc[dest_chain].sendrawtransaction(pegs_redeem_resp['hex'])


pegs_worstaccounts = rpc[dest_chain].pegsworstaccounts(pegs_txid)

pegs_exchange_resp = rpc[dest_chain].pegsexchange(pegs_txid, token_txid, gateways_amount)
txid = rpc[dest_chain].sendrawtransaction(pegs_exchange_resp['hex'])

pegs_worstaccounts = rpc[dest_chain].pegsworstaccounts(pegs_txid)

pegs_redeem = rpc[dest_chain].pegsredeem(pegs_txid, token_txid)

pegs_liquidate = rpc[dest_chain].pegsliquidate(pegs_txid, token_txid, WORST_ACCT_TXID)