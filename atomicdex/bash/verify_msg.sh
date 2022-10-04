#!/bin/bash
source userpass

curl --url "http://127.0.0.1:7783" --data "
{
  \"userpass\": \"$userpass\",
  \"method\": \"verify_message\",
  \"mmrpc\": \"2.0\",
  \"id\": 0,
  \"params\": {
    \"coin\": \"$1\",
    \"message\": \"$2\",
    \"signature\": \"$3\",
    \"address\": \"$4\"
  }
}"

