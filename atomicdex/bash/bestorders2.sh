source userpass
curl --url "http://127.0.0.1:7783" --data "{
	\"mmrpc\":\"2.0\",
	\"userpass\":\"$userpass\",
	\"method\":\"best_orders\",
	\"params\": {
		\"coin\":\"$1\",
		\"action\":\"$2\",
		\"volume\":$3
	}
	,\"id\":0
}"
