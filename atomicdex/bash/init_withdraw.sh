source userpass
curl --url "http://127.0.0.1:7783" --data "{
	\"mmrpc\":\"2.0\",
	\"userpass\":\"${userpass}\",
	\"method\":\"task::withdraw::init\",
	\"params\": {
		\"coin\":\"$1\",
		\"to\":\"$2\",
		\"amount\":\"$3\"
	}
	,\"id\":0
}"
