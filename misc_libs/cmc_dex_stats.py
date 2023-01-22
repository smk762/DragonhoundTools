#!/usr/bin/env python3
import requests
import sys
import os
import lib_cmc_api as cmc
from lib_color import colorize

def get_coins_config(branch='master'):
	return requests.get(f"https://raw.githubusercontent.com/KomodoPlatform/coins/{branch}/utils/coins_config.json").json()

def get_ticker(i):
	ticker = i['symbol']
	platform = None
	if i['platform']:
		platform = i['platform']['symbol']
		if i['platform']['symbol'] == "ETH":
			ticker = i['symbol']+"-ERC20"
		if i['platform']['symbol'] == "BNB":
			ticker = i['symbol']+"-BEP20"
		if i['platform']['symbol'] == "MATIC":
			ticker = i['symbol']+"-PLG20"
	return ticker, platform


if __name__ == '__main__':
	coins_data = get_coins_config()
	cmc_data = cmc.get_cmc_map()["data"]
	top_100_ids = []
	for coin in coins_data:
		coins_data[coin].update({
			"cmc_data": {}
		})

	cmc_dict = {}

	for i in cmc_data:
		ticker, platform = get_ticker(i)
		if i["rank"] <= 100:
			top_100_ids.append(str(i['id']))

		cmc_dict.update({ticker: i})

		cmc_dict[ticker].update({
			"listed_on_atomicdex": False,
			"coins_repo_data": {},
			"cmc_metadata": {},
			"platform": platform
		})

		if ticker in coins_data:
			coins_data[ticker].update({
				"cmc_id": i["id"],
				"cmc_rank": i["rank"],
				"cmc_slug": i["slug"],
				"cmc_platform": i["platform"]
			})
			cmc_dict[ticker].update({
				"listed_on_atomicdex": True,
				"coins_repo_data": coins_data[ticker]
			})

	cmc_listings = cmc.api('cryptocurrency/listings/latest', {}, 'v1')['data']
	
	for i in cmc_listings:
		ticker, platform = get_ticker(i)
		if ticker in cmc_dict:
			cmc_dict[ticker].update({
				"circulating_supply": i["circulating_supply"],
				"volume_24h": i["quote"]["USD"]["volume_24h"],
				"market_cap": i["quote"]["USD"]["market_cap"],
				"market_cap_volume_24h_ratio": round(i["quote"]["USD"]["volume_24h"] / i["quote"]["USD"]["market_cap"], 4),
			})

	top_100 = ','.join(top_100_ids)
	params = {"id": top_100}
	cmc_metadata = cmc.api('cryptocurrency/info', params, 'v2')['data']
	not_listed = 0
	listed = 0
	summary = {}
	for coin in cmc_dict:
		if cmc_dict[coin]["rank"] <= 100:

			if str(cmc_dict[coin]['id']) in cmc_metadata:
				cmc_dict[coin].update({"cmc_metadata": cmc_metadata[str(cmc_dict[coin]['id'])]})
				cmc_dict[coin].update({
					"website": cmc_metadata[str(cmc_dict[coin]['id'])]["urls"]["website"],
					"github": cmc_metadata[str(cmc_dict[coin]['id'])]["urls"]["source_code"]
				})

			summary.update({
				coin: {
					"rank": cmc_dict[coin]['rank'],
					"ticker": cmc_dict[coin]['symbol'],
					"platform": cmc_dict[coin]['platform'],
					"name": cmc_dict[coin]['name'],
					"market_cap": cmc_dict[coin]['market_cap'],
					"volume_24h": cmc_dict[coin]['volume_24h'],
					"ratio": cmc_dict[coin]['market_cap_volume_24h_ratio'],
					"website": cmc_dict[coin]['website'],
					"github": cmc_dict[coin]['github']
				}
			})


			if cmc_dict[coin]["listed_on_atomicdex"]:
				summary[coin].update({"listed": True})
				listed += 1
				# print(colorize(f"{summary[coin]}", 'green'))
			else:
				summary[coin].update({"listed": False})
				not_listed += 1
				print(colorize(f"{summary[coin]}", 'red'))

	print(f"In the top 100, {listed} are listed on AtomicDEX")

