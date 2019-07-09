pubkey=$(./get_pubkey.py)
echo $test2
if [[ ${#test2} -lt 80 ]]; then
        cd /home/smk762/FSM/komodo/src
	./komodod -addnode=45.77.192.213 -addnode=149.28.8.219 -addnode=149.28.253.160 -ac_supply=100000000 -ac_staked=99 -ac_name=ORACLEARTH  -pubkey=$pubkey -ac_reward=10000000000 -ac_cc=762 -ac_halving=762000 &

else
        echo "chain already running";
fi
sleep 30;
komodo-cli -ac_name=ORACLEARTH setgenerate true 0

