#!/bin/bash
test_rick=$(pgrep -a komodod | grep 'RICK')
mining = 1 # change to 0 for staking

username="smk762" # change this!
source /home/${username}/komodo/src/pubkey.txt

if [[ ${#test_rick} -lt 80 ]]; then
        echo "Starting RICK";
        /home/${username}/komodo/src/komodod -addnode=138.201.136.145 -addnode=95.217.44.58 -ac_supply=90000000000 -ac_staked=10 -ac_name=RICK -ac_reward=100000000 -ac_cc=3 -pubkey=$pubkey &
else
        /home/${username}/komodo/src/komodo-cli -ac_name=RICK setgenerate true $mining
        echo "RICK already running";
fi
