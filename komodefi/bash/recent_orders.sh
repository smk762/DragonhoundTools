source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"my_recent_swaps\",\"limit\":10}"
echo ""
