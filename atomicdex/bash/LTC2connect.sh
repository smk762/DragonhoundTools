#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"LTC\",\"servers\":[{\"url\":\"electrum1.cipig.net:10063\"}],\"address_format\":{\"format\":\"segwit\"},\"tx_history\":true}"
echo ""
