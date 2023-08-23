source userpass
curl --url "http://127.0.0.1:7783" --data '{"userpass":"'$userpass'", "method": "best_orders", "coin": "'$1'", "action": "sell", "volume": "'$2'"}'
echo ""
