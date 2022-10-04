#!/bin/bash
source userpass
echo 'curl --url "http://127.0.0.1:7783" --data "{\"method\":\"max_taker_vol\",\"coin\":\"'$1'\",\"trade_with\":\"'$2'\",\"userpass\":\"$userpass\",\"mm2\":1}"'
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"max_taker_vol\",\"coin\":\"$1\",\"trade_with\":\"$2\",\"userpass\":\"$userpass\",\"mm2\":1}"
echo ""
