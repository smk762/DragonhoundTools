#!/bin/bash
source userpass
#curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"sell\",\"base\":\"$1\",\"rel\":\"$2\",\"price\":\"$3\",\"volume\":\"$4\"}"
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"sell\",\"base\":\"$1\",\"rel\":\"$2\",\"price\":\"$3\",\"volume\":{\"numer\":\"2079937\",\"denom\":\"100000000\
