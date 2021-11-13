#!/usr/bin/env python3
import binance_api
import coinspot_api

print(binance_api.get_price('KMDBTC'))
print(coinspot_api.get_quote('buy','KMD','1'))
print(coinspot_api.get_quote('buy','BTC','1'))
print(coinspot_api.my_balances())