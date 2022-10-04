source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"my_tx_history\",\"coin\":\"$1\",\"limit\":10}"
echo ""
