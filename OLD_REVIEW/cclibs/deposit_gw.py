#!/usr/bin/env python3
from create_pegs import *

# Get Tokens Info
token_txid = rpc[pegs_chain].tokenlist()[0]
token_info = rpc[pegs_chain].tokeninfo(token_txid)
token_balance = rpc[pegs_chain].tokenbalance(token_txid)

print(colorize("Token Balance            ["+str(token_balance)+"]", 'green'))
print(colorize("Token TXID               ["+str(token_txid)+"]", 'green'))
print(colorize("Token owner pubkey       ["+str(token_info['owner'])+"]", 'green'))
print(colorize("Token Name               ["+str(token_info['name'])+"]", 'green'))
print(colorize("Token Supply             ["+str(token_info['supply'])+"]", 'green'))
print(colorize("Token Description        ["+str(token_info['description'])+"]", 'green'))

# Get Oracle Info
oracle_txid = rpc[pegs_chain].oracleslist()[0]
oracle_info = rpc[pegs_chain].oraclesinfo(oracle_txid)
print(colorize("Oracle TXID              ["+str(oracle_txid)+"]", 'green'))
print(colorize("Oracle Name              ["+str(oracle_info['name'])+"]", 'green'))
print(colorize("Oracle Description       ["+str(oracle_txid['description'])+"]", 'green'))
print(colorize("Oracle Format            ["+str(oracle_txid['format'])+"]", 'green'))
print(colorize("Oracle Publisher         ["+str(oracle_info['registered'][0]['publisher'])+"]", 'green'))
print(colorize("Oracle Funds             ["+str(oracle_info['registered'][0]['funds'])+"]", 'green'))


# Get Gateways Info
gw_txid = rpc[pegs_chain].gatewayslist()[0]
gw_info = rpc[pegs_chain].gatewaysinfo(gw_txid)
print(colorize("Gateways (Bind) TXID       ["+str(gw_txid)+"]", 'green'))
print(colorize("Gateways Name              ["+str(gw_info['name'])+"]", 'green'))
print(colorize("Gateways Pubkeys           ["+str(gw_info['pubkeys'])+"]", 'green'))
print(colorize("Gateways Oracle            ["+str(gw_info['oracletxid'])+"]", 'green'))
print(colorize("Gateways Token ID          ["+str(gw_info['tokenid'])+"]", 'green'))
print(colorize("Gateways Deposit Address   ["+str(gw_info['deposit'])+"]", 'green'))
print(colorize("Gateways Total Supply      ["+str(gw_info['totalsupply'])+"]", 'green'))
print(colorize("Gateways Remaining Supply  ["+str(gw_info['remaining'])+"]", 'green'))
print(colorize("Gateways Issued Supply     ["+str(gw_info['issued'])+"]", 'green'))

# Spawn the oraclefeed
spawn_oraclefeed(pegs_chain, komodod_path, oracle_txid, pegs_pubkey_1, gw_bind_txid)
time.sleep(60)

gw_deposit_amount = 0.1
gateways_data = deposit_gateway(pegs_chain, pegs_addr_1, pegs_pubkey_1,
                                 src_chain, src_addr, token_name,
                                 gw_deposit_amount, gw_bind_txid)
gw_deposit_txid = gateways_data [0]
coin_txid = [1]

# Create the Peg
resp = rpc[pegs_chain+"_2"].pegscreate(str(100), str(1), gw_bind_txid)
print(resp)
if 'hex' in resp:
    pegs_txid = rpc[pegs_chain+"_2"].sendrawtransaction(resp['hex'])
    wait_confirm(pegs_chain+"_2", pegs_txid)
    print(colorize("Pegs TXID                ["+str(pegs_txid)+"]", 'green'))
else:
    print(colorize("Pegs TXID failed!        ["+str(result)+"]", 'red'))
    exit(1)


# gdb -args /home/smk762/Mixa84/komodo/src/komdod -ac_name=PEGTEST -ac_supply=5000 -ac_reward=800000000", "-ac_sapling=1 -addnode=116.203.120.163  -addnode=116.203.120.91 -ac_cc=2 -ac_import=PEGSCC -ac_end=1 -ac_perc=0 -ac_cbopret=7
