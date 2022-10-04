#!/bin/bash
source userpass
port=7783
port=7788

curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"all_swaps_uuids_by_filter\",\"my_coin\":\"RICK\",\"other_coin\":\"BNBT\"}"
#curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"all_swaps_uuids_by_filter\",\"my_coin\":\"RICK\",\"from_timestamp\":1611705600}"
#curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"all_swaps_uuids_by_filter\",\"my_coin\":\"RICK\",\"from_timestamp\":1611705600,\"to_timestamp\":1641792001}"

echo ""
