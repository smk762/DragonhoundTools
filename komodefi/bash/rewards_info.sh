#!/bin/bash

source userpass

curl --url "http://127.0.0.1:7783/" --data "{
  \"userpass\":\"$userpass\",
  \"method\":\"kmd_rewards_info\"
}"
