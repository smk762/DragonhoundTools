#!/usr/bin/env python3
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *

rpc['TEST1'] = def_creds('TEST1')
notary_counts = {}
ntx_blocks = 0
blockheight = rpc['TEST1'].getblockcount()
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


