#!/bin/bash
source userpass
port=7783
port=7788
curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"setprice\",\"base\":\"$1\",\"rel\":\"$2\",\"price\":\"$3\",\"volume\":$4, \"save_in_history\":true}"
echo ""
