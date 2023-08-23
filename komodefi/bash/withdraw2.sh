#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"mmrpc\":\"2.0\",\"method\":\"withdraw\",\"params\":{\"coin\":\"$1\",\"to\":\"$2\",\"amount\":\"$3\"},\"id\":0}"

