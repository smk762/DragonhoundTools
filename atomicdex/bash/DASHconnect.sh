#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"DASH\",\"servers\":[{\"url\":\"electrum1.cipig.net:10061\"},{\"url\":\"electrum2.cipig.net:10061\"}]}"
