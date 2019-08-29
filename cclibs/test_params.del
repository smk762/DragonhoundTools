#!/usr/bin/env python3
import json

try:
    with open('test_config.json') as j:
        config = json.load(j)
except:
    print("No config.json file!")
    print("Create one using the 'test_config_example.json' template")
    sys.exit(0)
kmd_addr = config["kmd_addr"]
kmd_wif = config["kmd_wif"]
kmd_pub = config["kmd_pub"]
gateways_chain = config["gateways_chain"]
gateways_chain_params = config["gateways_chain_params"]
gateways_addr = config["gateways_addr"]
gateways_wif = config["gateways_wif"]
gateways_pub = config["gateways_pub"]
peg_token = config["peg_token"]
j.close()