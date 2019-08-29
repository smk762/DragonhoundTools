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
pegs_chain = "PEGSTEST"
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
pegs_launch_params.append("-earlytxid="+early_txid)
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
print(colorize("PEGTEST launch Params    ["+komodod_path+"/komodod "+''.join(pegs_launch_params)+"]", 'green'))

time.sleep(60)
rpc[pegs_chain].setgenerate(True, 1)
rpc[pegs_chain+"_2"].setgenerate(True, 1)

pegs_balance = rpc[pegs_chain].getbalance()
pegs_balance2 = rpc[pegs_chain+"_2"].getbalance()

# Create Tokens
tokensupply = 1 # Make user input. Does this need to be same (less?) than gw_deposit_amount?
tokensatsupply = int(100000000*tokensupply)
token_txid = token_create(pegs_chain, src_chain, tokensupply, "KMD_Tether")
print(colorize("Token TXID               ["+str(token_txid)+"]", 'green'))
token_balance = rpc[pegs_chain].tokenbalance(token_txid)['balance']
while int(token_balance) < 1:
    print("Waiting for token balance...")
    time.sleep(15)
    token_balance = rpc[pegs_chain].tokenbalance(token_txid)['balance']
    token_info = rpc[pegs_chain].tokeninfo(token_txid)
print(colorize("Token TXID               ["+str(token_txid)+"]", 'green'))
print(colorize("Token owner pubkey       ["+str(token_info['owner'])+"]", 'green'))
print(colorize("Token Name               ["+str(token_info['name'])+"]", 'green'))
print(colorize("Token Supply             ["+str(token_info['supply'])+"]", 'green'))
print(colorize("Token Description        ["+str(token_info['description'])+"]", 'green'))

# Create Oracle
#oracle_txid = create_oracle(pegs_chain, token_name, "blockheaders", "Ihh")
oracle_txid = create_oracle(pegs_chain, src_chain, "blockheaders", "Ihh")
oracle_info = rpc[pegs_chain].oraclesinfo(oracle_txid)
print(colorize("Oracle TXID              ["+str(oracle_txid)+"]", 'green'))
print(colorize("Oracle Publisher         ["+str(oracle_info['registered'][0]['publisher'])+"]", 'green'))

# Activate gateway binding
gateway_N = 1
gateway_M = 1
gw_bind_txid = bind_gateway(pegs_chain, token_txid, oracle_txid, src_chain, tokensatsupply,
             gateway_N, gateway_M, pegs_pubkey_1, 60, 85, 188)
gw_info = rpc[pegs_chain].gatewaysinfo(gw_bind_txid)
print(colorize("Oracle TXID      ["+str(gw_info['oracletxid'])+"]", 'green'))
print(colorize("Token TXID      ["+str(gw_info['tokenid'])+"]", 'green'))
print(colorize("Gateways (Bind) TXID      ["+str(gw_bind_txid)+"]", 'green'))
print(colorize("Gateways Coin ["+str(gw_info['coin'])+"]", 'green'))
print(colorize("Gateways Pubkeys ["+str(gw_info['pubkeys'])+"]", 'green'))
print(colorize("Gateways Deposit Address ["+str(gw_info['deposit'])+"]", 'green'))
print(colorize("Gateways Total Supply ["+str(gw_info['totalsupply'])+"]", 'green'))
print(colorize("Gateways Remaining Supply ["+str(gw_info['remaining'])+"]", 'green'))
print(colorize("Gateways Issued Supply ["+str(gw_info['issued'])+"]", 'green'))

# Spawn the oraclefeed
spawn_oraclefeed(pegs_chain, komodod_path, oracle_txid, pegs_pubkey_1, gw_bind_txid)
time.sleep(60)

# Gateway Deposit. Needs different pubkey?
#print("Creating new address and pubkey for gateway deposit.")
#pegs_addr_1B = rpc[pegs_chain].getnewaddress()
#pegs_wif_1B = rpc[pegs_chain].dumpprivkey(pegs_addr_1B)
#pegs_pubkey_1B = rpc[pegs_chain].validateaddress(pegs_addr_1B)['pubkey']
# gw_deposit_amount = 0.1 // try using tokensupply
gateways_data = deposit_gateway(pegs_chain, pegs_addr_1, pegs_pubkey_1,
                                 src_chain, src_addr, src_chain,
                                 tokensupply, gw_bind_txid)
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
