#!/bin/bash
source userpass
port=7783
port=7788
start=1612400504
end=1642400705
coin="RICK"
#curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"my_recent_swaps\",\"my_coin\":\"$1\",\"other_coin\":\"$2\"}"
curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"my_recent_swaps\",\"limit\":2,\"my_coin\":\"$coin\",\"from_timestamp\":$start,\"to_timestamp\":$end}"
#curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"my_recent_swaps\",\"limit\":2,\"my_coin\":\"KMD\",\"from_timestamp\":1611705600}"

echo ""
