#!/bin/bash
source userpass
while :; do curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"setprice\",\"base\":\"$1\",\"rel\":\"$2\",\"price\":\"$3\",\"volume\":\"$4\", \"cancel_previous\":false}"; sleep 1; done

