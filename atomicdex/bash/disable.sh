#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"disable_coin\",\"coin\":\"$1\"}"
echo ""
