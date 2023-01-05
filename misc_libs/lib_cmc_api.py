#!/usr/bin/env python3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

BASE_URL = 'https://pro-api.coinmarketcap.com/v1'
session = Session()
session.headers.update(HEADERS)

def get_cmc_map():
    params = {
        'start':'1',
        'sort':'cmc_rank',
    }
    resp = api("cryptocurrency/map", params)
    print(resp)
    with open('cmc_map.json', 'w+') as f:
        json.dump(resp['data'], f)

def api(endpoint, params):
    try:
        url = f'{BASE_URL}/{endpoint}'
        response = session.get(url, params=params)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None

if __name__ == '__main__':
    get_cmc_map()