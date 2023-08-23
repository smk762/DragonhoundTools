source userpass
curl --url "http://127.0.0.1:7783" --data "{
	\"mmrpc\":\"2.0\",
	\"userpass\":\"$userpass\",
	\"method\":\"orderbook\",
	\"params\": {
		\"base\":\"$1\",
		\"rel\":\"$2\"
	}
	,\"id\":42
}"
