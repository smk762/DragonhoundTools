#!/usr/bin/env python3
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cclibs'))
from oracleslib import *
timestamp = int(time.time())
ignore_nodes = []

ntx_oracles= {
            "LABS": "641bd59e9858f78eff5774b190b3d3e8da76b75b6cfae63ef0264487c2a3f52f",
            "CFEKMYLO": "a7e1e211f00f58760f77a22ec56b2c0460beb1cec76648fdef6794172579d259",
            "CFEKMYLO6": "7b5a255df1eddf6a27ccdebfba511ebe42082a7e2755e0d4cd4dbd1df25dcbd1",
            "CFEKOD": "a9c7878662e03c0d81d88dc21ad1afa9754fd38a58f849cfa65778bbed748373",
            "CFEKAPOW": "5867b76c1001ec0939a9062a6cd95f71c8a4d4e4e29f55a10e1847988e376dda"
    }
for chain in ntx_oracles:
    rpc[chain] = def_creds(chain)
    oracle_txid = ntx_oracles[chain]
    notary_counts = {}
    ntx_blocks = 0
    try:
        blockheight = rpc[chain].getblockcount()
        start_at = blockheight - 1440
        if start_at < 0:
                start_at = 1
        for x in range(start_at, blockheight):
                resp = rpc[chain].getNotarisationsForBlock(x)
                for ac in resp['LABS']:
                        if ac['chain'] == chain:
                                ntx_blocks += 1
                                for notary in ac['notaries']:
                                        if notary not in ignore_nodes:
                                                if str(notary) not in notary_counts:
                                                        notary_counts.update({str(notary):0})
                                                count = notary_counts[str(notary)]+1
                                                notary_counts.update({str(notary):count})
                                print("Block: "+str(x)+" | Txid: "+str(ac['txid'])+" | Hash: "+str(ac['blockhash']))
                time.sleep(0.01)

        print("Total notarised blocks: "+str(ntx_blocks))
        for notary in sorted(notary_counts.keys()):
                print(str(notary)+": "+str(notary_counts[notary]))
        notary_counts.update({"timestamp":timestamp})
        txid = write2oracle('ORACLEARTH', oracle_txid, str(notary_counts).replace("'", '"'))
        
        print(chain+" data written to "+ oracle_txid)
        print("TXID: "+txid)
    except Exception as e:
        print(e)
        print(oracle_txid)
        print(rpc[chain].oraclesinfo(oracle_txid))
        pass

