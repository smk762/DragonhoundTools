source userpass
curl --url "http://127.0.0.1:7783" --data '{
  "userpass":"'$userpass'",
  "method":"enable_slp",
  "mmrpc":"2.0",
  "params":{
    "ticker":"'$1'",
    "activation_params": {
      "required_confirmations": 3
    }
  }
}'
