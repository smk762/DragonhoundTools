source userpass
curl --url "http://127.0.0.1:7783" --data "{
	\"mmrpc\":\"2.0\",
	\"userpass\":\"$userpass\",
	\"method\":\"task::withdraw::cancel\",
	\"params\": {
		\"task_id\":$1
	}
	,\"id\":0
}"
