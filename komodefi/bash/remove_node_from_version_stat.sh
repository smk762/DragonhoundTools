source userpass
curl --url "http://127.0.0.1:7783" --data "{\"mmrpc\": \"2.0\",\"method\":\"remove_node_from_version_stat\",\"userpass\":\"$userpass\",\"params\":{\"name\": \"$1\"}}"
echo ""
