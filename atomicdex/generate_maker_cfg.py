#!/usr/bin/env python3
import os
import sys
import json
import requests
from dotenv import load_dotenv

# ENV VARS
load_dotenv()
MM2_USERPASS = os.getenv("MM2_USERPASS")
MM2_IP = "http://127.0.0.1:7783"
BIDIRECTIONAL_COINS = os.getenv("BIDIRECTIONAL_COINS").split(" ")
BUY_COINS = os.getenv("BUY_COINS").split(" ") + BIDIRECTIONAL_COINS
SELL_COINS = os.getenv("SELL_COINS").split(" ") + BIDIRECTIONAL_COINS
MIN_USD = os.getenv("MIN_USD")
MAX_USD = os.getenv("MAX_USD")
SPREAD = os.getenv("SPREAD")
ORDER_REFRESH_RATE = os.getenv("ORDER_REFRESH_RATE")
PRICES_API = os.getenv("PRICES_API")
PRICES_API_TIMEOUT = os.getenv("PRICES_API_TIMEOUT")
USE_BIDIRECTIONAL_THRESHOLD = os.getenv("USE_BIDIRECTIONAL_THRESHOLD") == "True"

ACTIVATE_COMMANDS = requests.get("http://116.203.120.91:8762/api/tools/mm2/get_enable_commands/").json()["commands"]

PARAMS = {
    "price_url": PRICES_API,
    "bot_refresh_rate": int(ORDER_REFRESH_RATE)	
}

CFG_TEMPLATE = {
    "base": "base_coin",
    "rel": "rel_coin",
    "min_volume": {
    	"usd":MIN_USD
    },
    "max_volume":  {
    	"usd":MAX_USD
    },
    "spread": SPREAD,
    "base_confs": 3,
    "base_nota": True,
    "rel_confs": 3,
    "rel_nota": True,
    "enable": True,
    "price_elapsed_validity": int(PRICES_API_TIMEOUT),
    "check_last_bidirectional_trade_thresh_hold": USE_BIDIRECTIONAL_THRESHOLD
}


def mm2_proxy(params):
  params.update({"userpass": MM2_USERPASS})
  #print(json.dumps(params))
  r = requests.post(MM2_IP, json.dumps(params))
  return r


def get_cfg(base,rel):
	cfg = CFG_TEMPLATE.copy()
	cfg.update({
	    "base": base,
	    "rel": rel,	
	})
	return cfg


if __name__ == '__main__':
	configs = {}
	for base in SELL_COINS:
		for rel in BUY_COINS:
			if base != rel:
				configs.update({
					f"{base}/{rel}": get_cfg(base, rel)
				})
	PARAMS.update({
		"cfg":configs
	})
	print(json.dumps(PARAMS, indent=4, sort_keys=True))
	
	with open('bot_configs.json', 'w', encoding='utf-8') as f:
		json.dump(PARAMS, f, ensure_ascii=False, indent=4)

	if len(sys.argv) > 1:
		if sys.argv[1] == "run":
			# activate coins
			for coin in list(set(BUY_COINS + SELL_COINS)):
				for protocol in ACTIVATE_COMMANDS:
					if coin in ACTIVATE_COMMANDS[protocol]:
						print(mm2_proxy(ACTIVATE_COMMANDS[protocol][coin]).json())

			command = {
			    "userpass": MM2_USERPASS,
			    "mmrpc": "2.0",
			    "method": "start_simple_market_maker_bot",
			    "params":PARAMS
		    }
			# start bot
			print(mm2_proxy(command).json())


