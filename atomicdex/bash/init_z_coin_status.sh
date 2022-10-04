#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "
{
    \"userpass\": \"${userpass}\",
    \"method\": \"task::enable_z_coin::status\",
    \"mmrpc\": \"2.0\",
    \"params\": {
        \"task_id\": $1
    }
}"
echo

