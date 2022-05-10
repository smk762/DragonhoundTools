Here's a list of potentially useful commands which have been mentioned in the Komodo Notary Node channel on Discord.

Shortcut to importing key into other chain, rescanning from 10 blocks before current tip:

`komodo-cli -ac_name=$chain importprivkey $(komodo-cli dumpprivkey $(komodo-cli listaddressgroupings|jq -r '.[][][0]')) "" true $(($(komodo-cli -ac_name=$chain getblockcount)-10))`


Splitting via iguana (change to your scriptPubKey):
```bash
~/komodo/src/listassetchains | while read chain; do
  unspent=$(~/komodo/src/komodo-cli -ac_name=${chain} listunspent | jq '[.[] | select (.generated==false and .amount==0.0001 and .spendable==true and (.scriptPubKey == "'210227e5cad3731e381df157de189527aac8eb50d82a13ce2bd81153984ebc749515ac'"))] | length')
  echo "${chain}: $unspent"
  if [ $unspent -lt 50 ]; then
    echo "Topping up ${chain}"
    curl --url "http://127.0.0.1:7776" --data "{\"coin\":\""${chain}"\",\"agent\":\"iguana\",\"method\":\"splitfunds\",\"satoshis\":\"10000\",\"sendflag\":1,\"duplicates\":"100"}"
  fi
done
```

Checks if chain running, launches if not:
```bash
test_rick=$(pgrep -a komodod | grep 'RICK')

username="YOUR_USERNAME" # change this!
source /home/${username}/rm_faucet/cron/pubkey.txt

echo $test_rick

if [[ ${#test_rick} -lt 80 ]]; then
        echo "Starting RICK";
        /home/${username}/komodo/src/komodod -addnode=138.201.136.145 -addnode=95.217.44.58 -ac_supply=90000000000 -ac_staked=10 -ac_name=RICK -ac_reward=100000000 -ac_cc=3 -pubkey=$pubkey &
else
        /home/${username}/komodo/src/komodo-cli -ac_name=RICK setgenerate true $mining
        echo "RICK already running";
fi
```

Checks if mining, and if not starts miner
```bash
test_mining=$(komodo-cli getgenerate | jq .numthreads)

if [[ ${test_mining} -lt 1 ]]; then
    komodo-cli setgenerate true 1
fi
```
