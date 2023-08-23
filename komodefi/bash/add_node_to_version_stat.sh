source userpass
curl --url "http://127.0.0.1:7783" --data "{\"mmrpc\": \"2.0\",\"method\":\"add_node_to_version_stat\",\"userpass\":\"$userpass\",\"params\":{\"name\": \"$1\",\"address\": \"$2\",\"peer_id\": \"$3\"}}"
echo ""
