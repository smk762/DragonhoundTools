#!/bin/bash
komodo-cli -ac_name=${1} stop
sleep 20
params=$(~/komodo/src/listassetchainparams | grep ${1})
source ~/komodo/src/pubkey.txt
echo $pubkey
echo $params
komodod $params -pubkey=$pubkey -reindex &

