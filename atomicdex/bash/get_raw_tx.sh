source userpass
curl --url "http://127.0.0.1:7783" --data "{
    \"mmrpc\": \"2.0\",
    \"method\":\"get_raw_transaction\",
    \"userpass\":\"$userpass\",
    \"params\":{\"coin\": \"$1\",
    \"tx_hash\": \"$2\"},
    \"id\":1
}"
