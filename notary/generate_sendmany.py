#!/usr/bin/env python3

import sys
import json
import requests

try:
    chain = sys.argv[1]
    season = sys.argv[2]
    server = sys.argv[3]
    amount = float(sys.argv[4])
except:
    print(e)
    print("Needs season, server, chain & amount params like 'generate_sendmany.py GLEEC Season_4 Third_Party 0.777'")
    sys.exit()

r = requests.get(f"http://116.203.120.91:8762/api/table/addresses/?season={season}&server={server}&chain={chain}")
resp = r.json()["results"]

addresses = []

for item in resp:
    addresses.append(item["address"])

sendmany = {}
for address in addresses:
    sendmany.update({address:amount})

print(chain+' sendmany "" "'+json.dumps(sendmany).replace('"', '\\"')+'"')
print(f"Sendmany generated for {len(resp)} {season} {server} addresses to send {amount}")
