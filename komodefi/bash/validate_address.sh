source userpass
curl --url "http://127.0.0.1:7783/" --data "{\"userpass\":\"$userpass\",\"method\":\"validateaddress\",\"coin\":\"$1\",\"address\":\"$2\"}"


echo ""
