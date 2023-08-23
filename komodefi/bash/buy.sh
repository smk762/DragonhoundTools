#!/bin/bash
source userpass
source port
curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"buy\",\"base\":\"$1\",\"rel\":\"$2\",\"price\":\"$3\",\"volume\":\"$4\"}"
echo ""
