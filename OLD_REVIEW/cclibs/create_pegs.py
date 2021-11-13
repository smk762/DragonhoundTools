#!/usr/bin/env python3
from gatewayslib import *
from pegslib import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'qa'))
from qalib import *
from oracleslib import *

# Get and set config
cwd = os.getcwd()
home = expanduser("~")

komodod_path = home+"/Mixa84/komodo/src"
src_chain = "KMD"
pegs_chain = "PEGSTEST"
token_name = src_chain+"T"

pegs_launch_params = launch_json[pegs_chain]['params']
pegs_launch_params_1 = pegs_launch_params[:]
pegs_launch_params_2 = pegs_launch_params[:]
pegs_secondary_datadir = home+'/.komodo2/'+pegs_chain

src_addr = addr_json['kmd_addr']
src_wif = addr_json['kmd_wif']
src_pubkey = addr_json['kmd_pubkey']
pegs_addr_1 = addr_json['pegs_addr_1']
pegs_wif_1 = addr_json['pegs_wif_1']
pegs_pubkey_1 = addr_json['pegs_pubkey_1']
pegs_addr_2 = addr_json['pegs_addr_2']
pegs_wif_2 = addr_json['pegs_wif_2']
pegs_pubkey_2 = addr_json['pegs_pubkey_2']

# Spawn two instances of a test chain
print("Spawning 2 Chainz")
pegsRPCs = spawn_2chainz(pegs_chain, pegs_launch_params, komodod_path,
                         pegs_pubkey_1, pegs_wif_1, pegs_pubkey_2, pegs_wif_2)

# Define RPC Proxies
rpc[src_chain] = def_creds(src_chain)
rpc[pegs_chain] = pegsRPCs[0]
rpc[pegs_chain+"_2"] = pegsRPCs[1]

# Launch Source Chain
launch_chain(src_chain, launch_json[src_chain]['params'], komodod_path,
             src_pubkey, src_wif)


pegs_balance = rpc[pegs_chain].getbalance()
pegs_balance2 = rpc[pegs_chain+"_2"].getbalance()

self_tx = rpc[pegs_chain].sendtoaddress(pegs_addr_1,int(pegs_balance/2))
wait_confirm(src_chain,self_tx)
# Create Tokens
gw_deposit_amount = 1
token_supply = 1000 
token_txid = token_create(pegs_chain, src_chain, token_supply, "KMD_Tether")
print(colorize("Token TXID               ["+str(token_txid)+"]", 'green'))
token_balance = rpc[pegs_chain].tokenbalance(token_txid)['balance']
while int(token_balance) < 1:
    print("Waiting for token balance...")
    time.sleep(15)
    token_balance = rpc[pegs_chain].tokenbalance(token_txid)['balance']
    token_info = rpc[pegs_chain].tokeninfo(token_txid)
while True:
    if 'supply' in token_info:
        token_sat_supply = token_info['supply']
        break
    print("Waiting for token supply")
    time.sleep(30)    
    print_tokeninfo(pegs_chain, token_txid)

# Create Oracle
#oracle_txid = create_oracle(pegs_chain, token_name, "blockheaders", "Ihh")
oracle_txid = create_oracle(pegs_chain, src_chain, "blockheaders", "Ihh")
print_oraclesinfo(pegs_chain, oracle_txid)

# Activate gateway binding
gateway_N = 1
gateway_M = 1
gw_bind_txid = bind_gateway(pegs_chain, token_txid, oracle_txid, src_chain,
                gateway_N, gateway_M, pegs_pubkey_1, 60, 85, 188)
print_gatewaysinfo(pegs_chain, gw_bind_txid)

# Spawn the oraclefeed
spawn_oraclefeed(pegs_chain, komodod_path, oracle_txid, pegs_pubkey_1, gw_bind_txid)
time.sleep(60)

#gateways_data = deposit_gateway(pegs_chain, pegs_addr_2, pegs_pubkey_2,
#                                 src_chain, src_addr, gw_deposit_amount, gw_bind_txid)
#gw_deposit_txid = gateways_data [0]
#coin_txid = [1]

# Create the Peg
pegs_funding = 100
num_binds = 1
resp = rpc[pegs_chain].pegscreate(str(pegs_funding), str(num_binds), gw_bind_txid)
print(resp)
if 'hex' in resp:
    pegs_txid = rpc[pegs_chain].sendrawtransaction(resp['hex'])
    wait_confirm(pegs_chain, pegs_txid)
    print(colorize("Pegs TXID                ["+str(pegs_txid)+"]", 'green'))
else:
    print(colorize("Pegs TXID failed!        ["+str(result)+"]", 'red'))
    exit(1)

early_txid = pegs_txid
pegs_launch_params.append("-earlytxid="+early_txid)
pegs_launch_params_1.append("-earlytxid="+early_txid)
pegs_launch_params_2.append("-earlytxid="+early_txid)
pegs_launch_params_2.append('-datadir='+pegs_secondary_datadir)
pegs_launch_params_2.append('-addnode=localhost')

print("Stopping Pegs chain 1, will restart with earlytxid in 1 minute.")
print("Stopping Pegs chain 2, will restart with earlytxid in 1 minute.")
rpc[pegs_chain].stop()
rpc[pegs_chain+"_2"].stop()
time.sleep(60)

print("Restarting PEGS chains with earlytxid")
launch_chain(pegs_chain, pegs_launch_params_1, komodod_path, pegs_pubkey_1)
launch_chain(pegs_chain+"_2", pegs_launch_params_2, komodod_path, pegs_pubkey_2)
print(colorize("PEGTEST launch Params    ["+komodod_path+"/komodod "+' '.join(pegs_launch_params)+"]", 'green'))

time.sleep(60)
rpc[pegs_chain].setgenerate(True, 1)
rpc[pegs_chain+"_2"].setgenerate(True, 1)

gateways_data = deposit_gateway(pegs_chain, pegs_addr_2, pegs_pubkey_2,
                                 src_chain, src_addr, gw_deposit_amount, gw_bind_txid)
gw_deposit_txid = gateways_data[0]
coin_txid = [1]

tokenbalance1 = rpc[pegs_chain].tokenbalance(token_txid)['balance']
tokenbalance2 = rpc[pegs_chain+"_2"].tokenbalance(token_txid)['balance']
print("Token Balance 1: "+str(tokenbalance1))
print("Token Balance 2: "+str(tokenbalance2))
print(pegs_chain+" balance 1: "+str(rpc[pegs_chain].getbalance()))
print(pegs_chain+" balance 2: "+str(rpc[pegs_chain+"_2"].getbalance()))

print("Claiming gateway...")
claim_txid = claim_gateway(pegs_chain, gw_bind_txid, src_chain, gw_deposit_txid,
                  pegs_pubkey_2, gw_deposit_amount)

tokenbalance1 = rpc[pegs_chain].tokenbalance(token_txid)['balance']
tokenbalance2 = rpc[pegs_chain+"_2"].tokenbalance(token_txid)['balance']
print("Token Balance 1: "+str(tokenbalance1))
print("Token Balance 2: "+str(tokenbalance2))
print(pegs_chain+" balance 1: "+str(rpc[pegs_chain].getbalance()))
print(pegs_chain+" balance 2: "+str(rpc[pegs_chain+"_2"].getbalance()))

pegsfund_hex = rpc[pegs_chain+"_2"].pegsfund(pegs_txid, token_txid, str(tokenbalance1['balance']))
if 'hex' in pegsfund_hex:
    pegsfund_txid = rpc[pegs_chain+"_2"].sendrawtransaction(pegsfund_hex['hex'])
else:
    print(pegsfund_hex)

pegsget_hex = rpc[pegs_chain+"_2"].pegsget(pegs_txid, token_txid, str(int(tokenbalance1['balance']/2)))
if 'hex' in pegsget_hex:
    pegsget_txid = rpc[pegs_chain+"_2"].sendrawtransaction(pegsget_hex['hex'])
else:
    print(pegsget_hex)

tokenbalance1 = rpc[pegs_chain].tokenbalance(token_txid)['balance']
tokenbalance2 = rpc[pegs_chain+"_2"].tokenbalance(token_txid)['balance']
print("Token Balance 1: "+str(tokenbalance1))
print("Token Balance 2: "+str(tokenbalance2))
print(pegs_chain+" balance 1: "+str(rpc[pegs_chain].getbalance()))
print(pegs_chain+" balance 2: "+str(rpc[pegs_chain+"_2"].getbalance()))

pegs_info = rpc[pegs_chain+"_2"].pegsinfo(pegs_txid)
print(pegs_info)

pegsacct_info = rpc[pegs_chain+"_2"].pegsaccountinfo(pegs_txid)
print(pegsacct_info)

pegsacct_history = rpc[pegs_chain+"_2"].pegsaccounthistory(pegs_txid)
print(pegsacct_history)

pegs_worstacct = rpc[pegs_chain+"_2"].pegsworstaccounts(pegs_txid)
print(pegs_worstacct)

pegsredeem_hex = rpc[pegs_chain+"_2"].pegsredeem(pegs_txid, token_txid)
if 'hex' in pegsredeem_hex:
    pegsredeem_txid = rpc[pegs_chain+"_2"].sendrawtransaction(pegsredeem_hex['hex'])
else:
    print(pegsredeem_hex)

rpc[pegs_chain+"_2"].sendtoaddress(pegs_addr_1, str(int(rpc[pegs_chain+"_2"].getbalance()/2)))

tokenbalance1 = rpc[pegs_chain].tokenbalance(token_txid)['balance']
tokenbalance2 = rpc[pegs_chain+"_2"].tokenbalance(token_txid)['balance']
print("Token Balance 1: "+str(tokenbalance1))
print("Token Balance 2: "+str(tokenbalance2))
print(pegs_chain+" balance 1: "+str(rpc[pegs_chain].getbalance()))
print(pegs_chain+" balance 2: "+str(rpc[pegs_chain+"_2"].getbalance()))

pegsexchange_txid = rpc[pegs_chain].pegsexchange(pegs_txid, token_txid, str(int(rpc[pegs_chain+"_2"].getbalance()/3)))
print(pegsexchange_txid)

pegs_worstacct = rpc[pegs_chain+"_2"].pegsworstaccounts(pegs_txid)
print(pegs_worstacct)

#pegs_liquidate = rpc[pegs_chain].pegsliquidate(pegs_txid, token_txid, account_txid)
#print(pegs_liquidate)

tokenbalance1 = rpc[pegs_chain].tokenbalance(token_txid)['balance']
tokenbalance2 = rpc[pegs_chain+"_2"].tokenbalance(token_txid)['balance']
print("Token Balance 1: "+str(tokenbalance1))
print("Token Balance 2: "+str(tokenbalance2))
print(pegs_chain+" balance 1: "+str(rpc[pegs_chain].getbalance()))
print(pegs_chain+" balance 2: "+str(rpc[pegs_chain+"_2"].getbalance()))