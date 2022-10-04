#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"DGB\",\"servers\":[{\"url\":\"electrum1.cipig.net:10059\"},{\"url\":\"electrum2.cipig.net:10059\"}]}"
