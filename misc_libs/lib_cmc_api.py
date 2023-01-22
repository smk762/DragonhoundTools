#!/usr/bin/env python3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import json
from dotenv import load_dotenv

load_dotenv()
CMC_API_KEY = os.getenv('CMC_API_KEY')
if len(CMC_API_KEY) == 0:
    print("You need to add an entry to your `.env` file for CMC_API_KEY")

HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API_KEY,
}

BASE_URL = 'https://pro-api.coinmarketcap.com'
session = Session()
session.headers.update(HEADERS)

def get_cmc_map():
    params = {
        'start':'1',
        'sort':'cmc_rank',
    }
    return api("cryptocurrency/map", params)    

def api(endpoint, params, api_version='v1'):
    try:
        url = f'{BASE_URL}/{api_version}/{endpoint}'
        response = session.get(url, params=params)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None

if __name__ == '__main__':
    resp = get_cmc_map()
    with open('cmc_map.json', 'w+') as f:
        print(resp)
        json.dump(resp['data'], f)