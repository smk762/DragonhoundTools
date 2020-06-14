#!/bin/bash
#pubkey=$(../shared/get_pubkey.py)
cd 
cd komodo
git pull
pkill -9 iguana
pubkey=022405dbc2ea320131e9f0c4115442c797bf0f2677860d46679ac4522300ce8c0a
chipsd -pubkey=$pubkey -addnode=74.208.210.191 -addnode=5.9.253.195 ${@} &
sleep 15
gamecreditsd -pubkey=$pubkey ${@} &
sleep 15
einsteiniumd -pubkey=$pubkey ${@} &
sleep 15
gincoind -pubkey=$pubkey ${@} &
sleep 15
aryacoind -pubkey=$pubkey ${@} &
#verusd -pubkey=$pubkey ${@} &
sleep 15
cd ~/Marmara-v.1.0/src
./komodod -ac_name=MCL -pubkey=$pubkey -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000 ${@} &
sleep 15
cd ~/hush3/src
./hushd -pubkey=$pubkey ${@} &
sleep 15
komodod -pubkey=$pubkey ${@} -notary &
sleep 300
cd ~/dpow/iguana
git pull
./m_notary_3rdparty
