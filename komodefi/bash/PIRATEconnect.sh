#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "
{
    \"userpass\": \"${userpass}\",
    \"method\": \"init_z_coin\",
    \"mmrpc\": \"2.0\",
    \"params\": {
        \"ticker\": \"ARRR\",
        \"activation_params\": {
            \"mode\": {
                \"rpc\": \"Light\",
                \"rpc_data\": {
                    \"electrum_servers\": [{\"url\":\"pirate.sirseven.me:10032\"}],
                    \"light_wallet_d_servers\": [\"http://pirate.sirseven.me:443\"]
                }
            }
        }
    }
}"
echo

