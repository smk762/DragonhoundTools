#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"MORTY\",\"tx_history\":true,\"servers\":[{\"url\":\"electrum1.cipig.net:10018\"},{\"url\":\"electrum2.cipig.net:10018\"}]}"
echo ""
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"RICK\",\"tx_history\":true, \"servers\":[{\"url\":\"electrum1.cipig.net:10017\"},{\"url\":\"electrum2.cipig.net:10017\"}]}"
echo ""
