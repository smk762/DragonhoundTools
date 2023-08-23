#!/bin/bash
source userpass
source port
curl --url "http://127.0.0.1:$port" --data "{\"userpass\":\"$userpass\",\"method\":\"cancel_all_orders\",\"cancel_by\":{\"type\":\"All\"}}"
echo ""
