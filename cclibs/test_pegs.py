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
addr_config = home+"/DragonhoundTools/config/test_addr.json"
launch_config = home+"/DragonhoundTools/config/launch_params.json"
src_chain = "KMD"
pegs_chain = "PEGTEST"
token_name = src_chain+"T"

# Get launch param configs
with open(launch_config) as launch_j:
    launch_json = json.load(launch_j)
pegs_launch_params = launch_json[pegs_chain]['params']
pegs_launch_params_1 = pegs_launch_params[:]
pegs_launch_params_2 = pegs_launch_params[:]

# Get Address configs
with open(addr_config) as addr_j:
    addr_json = json.load(addr_j)
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

bal = rpc[pegs_chain].getbalance()
early_txid = rpc[pegs_chain].sendtoaddress(pegs_addr_1, bal, "", "", True)
pegs_launch_params_1.append("-earlytxid="+early_txid)
pegs_launch_params_2.append("-earlytxid="+early_txid)

print("Stopping Pegs chain 1, will restart with earlytxid in 1 minute.")
print("Stopping Pegs chain 2, will restart with earlytxid in 1 minute.")
rpc[pegs_chain].stop()
rpc[pegs_chain+"_2"].stop()
time.sleep(60)

print("Restarting PEGS chains")
pegs_secondary_datadir = home+'/.komodo2/'+pegs_chain
pegs_launch_params_2.append('-datadir='+pegs_secondary_datadir)
pegs_launch_params_2.append('-addnode=localhost')
launch_chain(pegs_chain, pegs_launch_params_1, komodod_path, pegs_pubkey_1)
launch_chain(pegs_chain+"_2", pegs_launch_params_2, komodod_path, pegs_pubkey_2)

time.sleep(60)
rpc[pegs_chain].setgenerate(True, 1)

pegs_balance = rpc[pegs_chain].getbalance()
pegs_balance2 = rpc[pegs_chain+"_2"].getbalance()

# Create Tokens
tokensupply = 1000
tokensatsupply = 100000000*int(tokensupply)
token_txid = token_create(pegs_chain, token_name, tokensupply, "KMD_Tether")
wait_confirm(pegs_chain, token_txid)
tokeninfo = rpc[pegs_chain].tokeninfo(token_txid)
tokenbalance = rpc[pegs_chain].tokenbalance(token_txid, pegs_pubkey_1)

# Create Oracle
oracle_txid = create_oracle(pegs_chain, token_name, "blockheaders", "Ihh")
oracleinfo = rpc[pegs_chain].oraclesinfo(oracle_txid)

balance = rpc[pegs_chain].getbalance()
# Activate gateway binding
gateway_N = 1
gateway_M = 1
bind_txid = bind_gateway(pegs_chain, token_txid, oracle_txid, token_name, tokensatsupply,
             gateway_N, gateway_M, pegs_pubkey_1, 60, 85, 188)
wait_confirm(pegs_chain, bind_txid)
gw_info = rpc[pegs_chain].gatewaysinfo(bind_txid)
gw_deposit_addr = gw_info['deposit']

# Spawn the oraclefeed
spawn_oraclefeed(pegs_chain, komodod_path, oracle_txid, pegs_pubkey_1, bind_txid)
time.sleep(60)

# Deposit to gateway
gw_deposit_amount = 0.1

# create new address, otherwise gw dep addr is same as pegs addr, 
# and gateways deposit wil not validate
pegs_addr_1B = rpc[pegs_chain].getnewaddress()
pegs_wif_1B = rpc[pegs_chain].dumpprivkey(pegs_addr_1B)
pegs_pubkey_1B = rpc[pegs_chain].validateaddress(pegs_addr_1B)['pubkey']

print("Pegs Token Address created")
print("pegs_addr_1B: "+pegs_addr_1B)
print("pegs_wif_1B: "+pegs_wif_1B)
print("pegs_pubkey_1B :"+pegs_pubkey_1B)

gw_deposit_addr = rpc[pegs_chain+"_2"].gatewaysinfo(bind_txid)['deposit']
print(colorize("Gateways Deposit Address ["+str(gw_deposit_addr)+"] created", 'green'))
txid = rpc[src_chain].sendtoaddress(src_addr, float(gw_deposit_amount*2))
wait_confirm(src_chain, txid)


op_id = rpc[src_chain].z_sendmany(src_addr, [{"address":pegs_addr_2, "amount":0.0001},
                        {"address":gw_deposit_addr, "amount":gw_deposit_amount}])
op_status = rpc[src_chain].z_getoperationstatus([op_id])
while op_status[0]['status'] != 'success':
    print(op_status)
    time.sleep(15)
    op_status = rpc[src_chain].z_getoperationstatus([op_id])
coin_txid = op_status[0]['result']['txid']
print(colorize("Coin TXID ["+str(bind_txid)+"] created", 'green'))
wait_confirm(src_chain, coin_txid)
tx_info = rpc[src_chain].gettransaction(coin_txid)
# print(tx_info)
#for account in tx_info['details']:
 #   if account['address'] == pegs_addr_1:
  #      claim_vout = account['vout']
claim_vout = 0
deposithex = tx_info['hex']
tx_blockhash = tx_info['blockhash']
height = rpc[src_chain].getblock(tx_blockhash)['height']
proof = rpc[src_chain].gettxoutproof([coin_txid])
print("~/Mixa84/komodo/src/komodo-cli -ac_name="+pegs_chain \
    +" gatewaysdeposit "+bind_txid+" "+str(height)+" "+ src_chain \
            +" "+coin_txid+" "+str(claim_vout)+" "+deposithex, proof \
            +" "+pegs_pubkey_2+" "+str(gw_deposit_amount))
resp = rpc[pegs_chain+"_2"].gatewaysdeposit(bind_txid, str(height), token_name,
                                 coin_txid, str(claim_vout),
                                 deposithex, proof,
                                 pegs_pubkey_2, str(gw_deposit_amount))
while resp['result'] == 'error':
    print(resp['error'])
    print("waiting for notarisation")
    print(pegs_pubkey_2)
    print(rpc[pegs_chain+"_2"].getinfo()['pubkey'])
    time.sleep(20)
    resp = rpc[pegs_chain+"_2"].gatewaysdeposit(bind_txid, str(height), token_name,
                                 coin_txid, str(claim_vout),
                                 deposithex, proof,
                                 pegs_pubkey_2, str(gw_deposit_amount))
print(resp)
gw_deposit_txid = rpc[pegs_chain+"_2"].sendrawtransaction(resp['hex'])
wait_confirm(pegs_chain+"_2", gw_deposit_txid)
#return gw_deposit_txid, coin_txid

# Create the Peg
resp = rpc[pegs_chain+"_2"].pegscreate(str(100), str(1), bind_txid)
pegs_txid = rpc[pegs_chain+"_2"].sendrawtransaction(resp['hex'])
wait_confirm(pegs_chain+"_2", pegs_txid)

print("Pegs TXID: "+pegs_txid)
print("Coin TXID: "+coin_txid)
print("Bind TXID: "+bind_txid)
print("Gateways Deposit TXID: "+gw_deposit_txid)
print("Early TXID: "+early_txid)
print("PEGTEST launch Params: "+str(pegs_launch_params_1))

print(komodod_path+"/komodo-cli =ac_name="+pegs_chain+" gatewaysclaim "+bind_txid+" "+token_name+" "+str(gw_deposit_txid)+" "+pegs_pubkey_1+" "+str(gw_deposit_amount))
resp = rpc[pegs_chain+"_2"].gatewaysclaim(bind_txid, token_name,
                             gw_deposit_txid, 
                             pegs_pubkey_2, str(gw_deposit_amount))

print(resp)
gw_claim_txid = rpc[pegs_chain+"_2"].sendrawtransaction(resp['hex'])
wait_confirm(pegs_chain+"_2", gw_claim_txid)
print(komodod_path+"/komodo-cli =ac_name="+pegs_chain+" pegsfund "+pegs_txid+" "+token_txid+" "+str(gw_deposit_amount))
resp = rpc[pegs_chain+"_2"].pegsfund(pegs_txid, token_txid, str(gw_deposit_amount))
print(resp)
pegs_fund_txid = rpc[pegs_chain+"_2"].sendrawtransaction(pegs_fund_resp['hex'])
print("Gateways Claim TXID: "+gw_claim_txid)
print("Pegs Fund TXID: "+pegs_fund_txid)

# gdb -args /home/smk762/Mixa84/komodo/src/komdod -ac_name=PEGTEST -ac_supply=5000 -ac_reward=800000000", "-ac_sapling=1 -addnode=116.203.120.163  -addnode=116.203.120.91 -ac_cc=2 -ac_import=PEGSCC -ac_end=1 -ac_perc=0 -ac_cbopret=7
