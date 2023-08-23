source userpass
curl --url "http://127.0.0.1:7783" --data "{
    \"method\": \"get_current_mtp\",
    \"userpass\": \"$userpass\",
    \"mmrpc\": \"2.0\",
    \"id\": 2,
    \"params\": {
        \"coin\": \"$1\"
    }
}"
echo ""
