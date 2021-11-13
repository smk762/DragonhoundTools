#!/usr/bin/env python3
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *

ignore_nodes = [4]
testnodes = ['TEST2FAST','TEST2FAST2','TEST2FAST3','TEST2FAST4','TEST2FAST5','TEST2FAST6']

print(" --------------------------------- ")

notary_counts = {}
ntx_blocks = 0
for node in testnodes:
	rpc[node] = def_creds(node)
	blockheight = rpc[node].getblockcount()
	start_at = 1
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

num_nn = 0
count_list = []
sum_count = 0
max_count = 0
min_count = 99999999
for notary in sorted(notary_counts.keys()):
	print(str(notary)+": "+str(notary_counts[notary]))
	if notary_counts[notary] > max_count:
		max_count = notary_counts[notary]
	if notary_counts[notary] < min_count:
		min_count = notary_counts[notary]
	sum_count += notary_counts[notary]
	num_nn += 1

	count_list.append(notary_counts[notary])
ave = sum_count/num_nn
med_index = int(len(count_list)/2)
count_list.sort()
print("ALL CHAINS: "+node)
print(notary_counts)
print("Min: "+str(min_count))
print("Max: "+str(max_count))
print("Ave: "+str(ave))
print("Median: "+str(count_list[med_index]))

print(" --------------------------------- ")