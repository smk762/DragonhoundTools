#!/bin/bash
source userpass
while :
do
date
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"max_taker_vol\",\"coin\":\"$1\",\"trade_with\":\"$2\",\"userpass\":\"$userpass\",\"mm2\":1}"
echo ""
sleep 5
done
