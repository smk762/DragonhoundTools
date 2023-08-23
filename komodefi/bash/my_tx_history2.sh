source userpass
curl --url "http://127.0.0.1:7783" --data "{
  \"userpass\":\"$userpass\",
  \"method\":\"my_tx_history\",
  \"mmrpc\":\"2.0\",
  \"params\": {
    \"coin\": \"$1\"
  }
}"
echo ""
