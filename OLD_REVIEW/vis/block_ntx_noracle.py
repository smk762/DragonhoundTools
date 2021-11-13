#!/usr/bin/env python3
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *

ignore_nodes = []
testnodes = ['TEST2FAST','TEST2FAST2','TEST2FAST3','TEST2FAST4','TEST2FAST5','TEST2FAST6']
for node in testnodes:
	rpc[node] = def_creds(node)
	notary_counts = {}
	ntx_blocks = 0
	blockheight = rpc[node].getblockcount()
	start_at = blockheight - 1440
	for x in range(start_at, blockheight):
		resp = rpc[node].getNotarisationsForBlock(x)
		for chain in resp['LABS']:
			if chain['chain'] == node:
				ntx_blocks += 1
				for notary in chain['notaries']:
					if notary not in ignore_nodes:
						if str(notary) not in notary_counts:
							notary_counts.update({str(notary):0})
						count = notary_counts[str(notary)]+1
						notary_counts.update({str(notary):count})
		time.sleep(0.01)
	print("Total notarised blocks: "+str(ntx_blocks))
	for notary in sorted(notary_counts.keys()):
		print(str(notary)+": "+str(notary_counts[notary]))

	notary_counts.update({"timestamp":int(time.time())})
	print("CHAIN: "+node)
	print(notary_counts)

	print(" --------------------------------- ")

testnodes = ['TEST2FAST','TEST2FAST2','TEST2FAST3','TEST2FAST4','TEST2FAST5','TEST2FAST6']
notary_counts = {}
ntx_blocks = 0
for node in testnodes:
	rpc[node] = def_creds(node)
	blockheight = rpc[node].getblockcount()
	start_at = blockheight - 1440
	for x in range(start_at, blockheight):
		resp = rpc[node].getNotarisationsForBlock(x)
		for chain in resp['LABS']:
			if chain['chain'] == node:
				ntx_blocks += 1
				for notary in chain['notaries']:
					if notary not in ignore_nodes:
						if str(notary) not in notary_counts:
							notary_counts.update({str(notary):0})
						count = notary_counts[str(notary)]+1
						notary_counts.update({str(notary):count})
		time.sleep(0.01)
	print("Total notarised blocks: "+str(ntx_blocks))
	for notary in sorted(notary_counts.keys()):
		print(str(notary)+": "+str(notary_counts[notary]))

	notary_counts.update({"timestamp":int(time.time())})
print("ALL CHAINS: "+node)
print(notary_counts)
print(" --------------------------------- ")