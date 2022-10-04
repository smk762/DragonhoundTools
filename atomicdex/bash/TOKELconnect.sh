#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"TOKEL\",\"servers\":[{\"url\":\"1.eu.tokel.electrum.dexstats.info:10077\"}]}"
