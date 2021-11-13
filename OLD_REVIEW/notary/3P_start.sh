#!/bin/bash
pubkey=$(cat config.json | jq .pubkey)

chipsd -pubkey=$pubkey -addnode=74.208.210.191 -addnode=5.9.253.195 ${@} &
sleep 60
gamecreditsd -pubkey=$pubkey ${@} &
sleep 60
einsteiniumd -pubkey=$pubkey ${@} &
sleep 60
gincoind -pubkey=$pubkey ${@} &
sleep 60
verusd -pubkey=$pubkey ${@} &
sleep 60
komodod -notary -pubkey=$pubkey ${@} &
