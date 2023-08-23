source userpass
curl --url "http://127.0.0.1:7783" --data '{
  "userpass":"'$userpass'",
  "method":"enable_bch_with_tokens",
  "mmrpc":"2.0",
  "params":{
    "ticker":"BCH",
    "allow_slp_unsafe_conf":false,
    "bchd_urls":[
      "https://bchd.imaginary.cash:8335/"
    ],
    "mode":{
      "rpc":"Electrum",
      "rpc_data":{
        "servers":[
          {
            "url":"electrum1.cipig.net:10055"
          },
          {
            "url":"electrum2.cipig.net:10055"
          },
          {
            "url":"electrum3.cipig.net:10055"
          },
          {
            "url":"electrum1.cipig.net:20055",
            "protocol": "SSL"
          },
          {
            "url":"electrum2.cipig.net:20055",
            "protocol": "SSL"
          },
          {
            "url":"electrum3.cipig.net:20055",
            "protocol": "SSL"
          }
        ]
      }
    },
    "tx_history":true,
    "slp_tokens_requests":[
      {
        "ticker":"ASLP",
        "required_confirmations": 4
      }
    ],
    "required_confirmations":5,
    "requires_notarization":false,
    "address_format":{
      "format":"cashaddress",
      "network":"bitcoincash"
    },
    "utxo_merge_params":{
      "merge_at":50,
      "check_every":10,
      "max_merge_at_once":25
    }
  }
}'
