#!/usr/bin/env python3
from kmdlib import *

def checkgenerate(coin):
    gen = rpc[coin].getgenerate()
    print("Staking :"+str(gen['staking']))
    print("Mining :"+str(gen['generate']))
    print("Threads :"+str(gen['numthreads']))

def segid_status(coin):
    segid_list = []
    segids = {}
    unspent = rpc[coin].listunspent()
    checkgenerate(coin)
    print(str(len(unspent))+" unspent utxos for "+coin)
    for utxo in unspent:
        if utxo['segid'] not in segid_list:
            segid_list.append(utxo['segid'])
            segids[utxo['segid']] = {}
            segids[utxo['segid']]['count'] = 1
            segids[utxo['segid']]['addresses'] = [utxo['address']]
            segids[utxo['segid']]['value'] = utxo['amount']
        else:
            segids[utxo['segid']]['value'] += utxo['amount']
            if utxo['address'] not in segids[utxo['segid']]['addresses']:
                segids[utxo['segid']]['count'] += 1
                segids[utxo['segid']]['addresses'].append(utxo['address'])
    print(str(len(segid_list))+"/64 SegIDs used")
    for segid in segids:
        output = str(segid)+" : "
        output += str(segids[segid]['value'])+" in "
        output += str(segids[segid]['count'])+" addresses "
        output += str(segids[segid]['addresses'])
        print(output)
    return segids

def check_mining_state()
    src_chain = selectRangeInt(1,len(assetchains),"Select chain: ")
    rpc_connection = def_credentials(assetChains[src_chain-1])
    chain_status=rpc_connection.getgenerate()
    if chain_status['generate']: 
        if int(chain_status['numthreads']) == 0:
            status = assetChains[src_chain-1]+" is staking"
        else:
            status = assetChains[src_chain-1]+" is mining with "+str(chain_status['numthreads'])+" threads"
    else:
        status =  assetChains[src_chain-1]+" is idle"
    print('Status: '+status)
    chain_balance=rpc_connection.getbalance()
    print('Balance: '+str(chain_balance))
    gen_states=['mining on', 'staking on', 'mining/staking off', 'exit' ]

    ID=1
    for state in gen_states:
        print(str(ID).rjust(3) + ' | ' + gen_states[ID-1].ljust(12))
        ID+=1
        assetChains.append(chain['ac_name'])

    gen_option = selectRangeInt(1,len(gen_states),"Select option: ")
    if gen_option == 1:
        numthreads = selectRangeInt(1,max_threads,"How many threads (max "+str(max_threads)+"): ")
        print('starting miner')
        rpc_connection.setgenerate(True, numthreads)
    elif gen_option == 2:   
        print('starting staker')
        rpc_connection.setgenerate(True, 0)
    elif gen_option == 3:   
        print('stopping mining/staking')
        rpc_connection.setgenerate(False)
    elif gen_option == 4:
        print('Goodbye!')
        exit(1)
    else:
        print('Invalid selection!')
        exit(1)
    time.sleep(2)
    chain_status=rpc_connection.getgenerate()
    if chain_status['generate']: 
        if int(chain_status['numthreads']) == 0:
            status = assetChains[src_chain-1]+" is staking"
        else:
            status = assetChains[src_chain-1]+" is mining with "+str(chain_status['numthreads'])+" threads"
    else:
        status =  assetChains[src_chain-1]+" is idle"
    print('Status: '+status)
    chain_balance=rpc_connection.getbalance()
    print('balance: '+str(chain_balance))