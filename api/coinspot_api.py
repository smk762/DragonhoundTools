#!/usr/bin/env python3
import os
from os.path import expanduser
import time
import json
import hmac
import hashlib
import requests
from urllib.parse import urljoin, urlencode

# Get and set config
cwd = os.getcwd()
home = expanduser("~")

with open(home+"/DragonhoundTools/api/api_keys.json") as keys_j:
    keys_json = json.load(keys_j)

api_key = keys_json['coinspot_key']
api_secret = keys_json['coinspot_secret']
base_url = 'https://www.coinspot.com.au'

headers = {
    'key': api_key,
    'Content-type': 'application/json',
    'Accept': 'text/plain'
}

def get_api_response(headers, params, endpoint):
	print(endpoint)
	nonce = int(time.time()*time.time())
	params['nonce'] = str(nonce)
	#print(params)
	#query_string = urlencode(params)
	#print(query_string)
	query_string = json.dumps(params, separators=(',', ':'))
	print(query_string)
	headers['sign'] = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha512).hexdigest()
	r = requests.post(endpoint, headers=headers, params=params)
	if r.status_code == 200:
	    return json.dumps(r.json(), indent=2)
	else:
	    return ("Error: "+str(r.status_code)+" , "+r.text)

def get_quote(quote_type, ticker, amount):
	api_path = '/api/quote/'+quote_type # buy or sell
	params = {
	    'cointype': ticker,
	    'amount': amount
	}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp

def get_deposit_addr(ticker):
	api_path = '/api/my/coin/deposit'
	params = {
	    'cointype': ticker
	}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp

def withdraw(ticker, address, amount):
	api_path = '/api/my/coin/send'
	params = {
	    'cointype': ticker,
	    'address': address,
	    'amount': amount
	}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp

def my_balances():
	api_path = '/api/my/balances'
	params = {}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp

def my_orders():
	api_path = '/api/my/orders'
	params = {}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp

def buy(ticker, amount, rate):
	api_path = '/api/my/buy'
	params = {
	    'cointype': ticker,
	    'amount': amount,
	    'rate': rate,
	}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp

def sell(ticker, amount, rate):
	api_path = '/api/my/sell'
	params = {
	    'cointype': ticker,
	    'amount': amount,
	    'rate': rate,
	}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp

def cancel(order_type, order_id):
	api_path = '/api/my/'+order_type+'/cancel' 
	params = {
	    'id': order_id
	}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp

def get_orderbook(ticker):
	api_path = '/api/orders' 
	params = {
	    'cointype': ticker
	}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp

def orderbook_history(ticker):
	api_path = '/api/orders/history' 
	params = {
	    'cointype': ticker
	}
	url = urljoin(base_url, api_path)
	resp = get_api_response(headers, params, url)
	return resp
