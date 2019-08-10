#!/usr/bin/env python3
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cclibs'))
from oracleslib import *

oracle_txid = '15d8de2ab39639010ae4373351ff50192311943b1817bbb53873ff64d7964aa0'
rpc['TEST1'] = def_creds('TEST1')
notary_counts = {}
ntx_blocks = 0
blockheight = rpc['TEST1'].getblockcount()
start_at = blockheight - 1440
for x in range(4000, blockheight):
	resp = rpc['TEST1'].getNotarisationsForBlock(x)
	for chain in resp['LABS']:
		if chain['chain'] == 'TEST1':
			ntx_blocks += 1
			for notary in chain['notaries']:
				if str(notary) not in notary_counts:
					notary_counts.update({str(notary):0})
				count = notary_counts[str(notary)]+1
				notary_counts.update({str(notary):count})
			print("Block: "+str(x)+" | Txid: "+str(chain['txid'])+" | Hash: "+str(chain['blockhash']))			
	time.sleep(0.01)
print("Total notarised blocks: "+str(ntx_blocks))
for notary in sorted(notary_counts.keys()):
	print(str(notary)+": "+str(notary_counts[notary]))

write2oracle('ORACLEARTH', oracle_txid, str(notary_counts))
