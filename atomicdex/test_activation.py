#!/usr/bin/env python3
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
MM2_USERPASS = os.getenv("MM2_USERPASS")
MM2_IP = "http://127.0.0.1:7783"

def mm2_proxy(params):
  params.update({"userpass": MM2_USERPASS})
  #print(json.dumps(params))
  r = requests.post(MM2_IP, json.dumps(params))
  return r

activate_commands = requests.get("http://stats.kmd.io/api/atomicdex/activation_commands/").json()["commands"]

error_coins = []
coins_count = 0
coins_responding_count = 0
errors = {}
coins_with_balance = {}
bad_electrums = ["tBLK", "GIN", "LYNX", "PGT", "CIPHS", "VOTE2021", "HUSH3"]
ignore_coins = bad_electrums
for protocol in activate_commands:
	for coin in activate_commands[protocol]:
		if coin not in ignore_coins:
			coins_count += 1
			try:
				resp = mm2_proxy(activate_commands[protocol][coin]).json()
				if "balance" not in resp:
					errors.update({coin:{
						"error":resp,
						"command":activate_commands[protocol][coin],
						}
					})
					print("---------------------------")
					print(f"{coin}: no balance, {resp}")
					error_coins.append(coin)
					print(activate_commands[protocol][coin])
					print("---------------------------")
				else:
					coins_responding_count += 1
					if float(resp["balance"]) > 0:
						coins_with_balance.update({
							coin: {
								"address":resp["address"],
								"balance":resp["balance"],
							}
						})
					#else:
						#print(f"{coin} OK: Balance = {resp['balance']}")
			except Exception as e:
				print("---------------------------")
				error_coins.append(coin)
				errors.update({coin:{
					"error":e,
					"command":activate_commands[protocol][coin],
					}
				})
				print(f"{coin}: {e}")
				print(activate_commands[protocol][coin])
				print("---------------------------")

print("")
print(errors)
print("")

print("")
print(error_coins)
print("")

print(coins_with_balance)
print("")

print(f"{coins_count} coins scanned")
print(f"{coins_responding_count}/{coins_count} coins returned response")
print(f"{len(coins_with_balance)}/{coins_count} coins with a balance")
