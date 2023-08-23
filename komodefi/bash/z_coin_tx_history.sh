source userpass
curl --url "http://127.0.0.1:7783" --data "{
  \"userpass\":\"$userpass\",
  \"method\":\"z_coin_tx_history\",
  \"mmrpc\":\"2.0\",
  \"params\": {
    \"coin\": \"$1\",
    \"limit\": 50
  }
}"
echo ""
