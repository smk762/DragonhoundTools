source userpass
source port
curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"update_maker_order\",\"uuid\":\"$1\",\"new_price\":\"$2\",\"volume_delta\":\"$3\"}"
echo ""
