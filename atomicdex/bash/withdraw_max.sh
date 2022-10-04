#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"withdraw\",\"coin\":\"$1\",\"to\":\"$2\",\"userpass\":\"$userpass\", \"max\":true}"

