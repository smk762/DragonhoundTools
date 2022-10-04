source userpass
source port
curl --url "http://127.0.0.1:$port" --data "{\"method\":\"version\",\"userpass\":\"$userpass\"}"
echo ""
