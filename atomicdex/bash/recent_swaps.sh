#!/bin/bash
source userpass
port=7783
port=7788
curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"my_recent_swaps\",\"page_number\":3,\"limit\":2}"

echo ""
