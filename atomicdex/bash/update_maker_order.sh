#!/bin/bash
source userpass
#curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"DGB\",\"servers\":[{\"url\":\"electrum1.cipig.net:10059\"},{\"url\":\"electrum2.cipig.net:10059\"}]}"
#curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"update_maker_order\",\"uuid\":\"$1\",\"new_price\":\"$2\",\"volume_delta\":\"$3\"}"
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"update_maker_order\",\"uuid\":\"$1\",\"new_price\":\"$2\"}"
echo
