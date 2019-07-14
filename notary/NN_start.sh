#!/bin/bash
source ~/komodo/src/pubkey.txt
bitcoind -deprecatedrpc=estimatefee &
#~/VerusCoin/src/verusd -pubkey=$pubkey &
~/hush3/src/hushd -pubkey=$pubkey &
sleep 60
cd ~/komodo/src
./komodod -gen -genproclimit=1 -notary -pubkey=$pubkey &
sleep 600
#./assetchains.old
./assetchains
