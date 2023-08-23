source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"unban_pubkeys\",\"unban_by\":{\"type\":\"All\"}}"
echo ""
