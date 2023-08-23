#!/bin/bash
source userpass
for i in {1..400}
do
  curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"setprice\",\"base\":\"$1\",\"rel\":\"$2\",\"price\":\"$3\",\"volume\":$4, \"cancel_previous\":true}"
  echo ""
  sleep 60
done
