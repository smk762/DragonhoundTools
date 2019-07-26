#!/bin/bash
params=$(~/komodo/src/listassetchainparams | grep ${1})
source ~/komodo/src/pubkey.txt
echo $pubkey
echo $params
komodod $params -pubkey=$pubkey &

