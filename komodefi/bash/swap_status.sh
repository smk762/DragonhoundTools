#!/bin/bash
source userpass
port=7783
port=7788
curl --url "http://127.0.0.1:$port" --data "{\"method\":\"my_swap_status\",\"params\":{\"uuid\":\"$1\"},\"userpass\":\"$userpass\"}"
echo
