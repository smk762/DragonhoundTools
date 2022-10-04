source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"recover_funds_of_swap\",\"params\":{\"uuid\":\"$1\"}}"
echo ""

