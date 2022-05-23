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

# Dust Attack Recovery

To check if you affected or not:

`time (~/komodo/src/komodo-cli listunspent | jq '. | { "utxos" : length }' && ~/komodo/src/komodo-cli getwalletinfo | jq '{ "txcount" : .txcount }') | jq -s add`

If you'll see > 1000 utxos - you are affected. To merge all your utxos into one, use the following snippet few times:

`~/komodo/src/komodo-cli z_mergetoaddress '["ANY_TADDR"]' %YOUR_NOTARY_ADDRESS% 0.0001 0 0`

# System load
```bash
#!/bin/sh
free -m | awk 'NR==2{printf "RAM: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'
df -h | awk '$NF=="/"{printf "HDD: %d/%dGB (%s)\n", $3,$2,$5}'
top -bn1 | grep load | awk '{printf "CPU: %.2f\n", $(NF-2)}' 
```


# Quick rescan (from Shossain)
```bash
./komodo-cli z_importkey "secret-extended-key-main1qwz9ku3nqqqqpqpdh0a7ny03ql3svcr8pqartwk77ckqpx00mysg0s488338yng2mjy3rp2zkav9ztmmvrp0j3daheuxuz2eg8jn93wzuzp6cekzrznq8v28td273aajger7xvjp7j43g00n25qc6nfrjtz5q9qrm5jrznq8k8pytprvl7m680w2787wntg8exwnv09xs95cmcze9tayfxay2cgeylwrw2xqhmjkxd8m3zvgzeyjdte3ypcaax7muv04u725jazuttsh52exn" "yes" 2918300
# this z-addr key is just a generic one and doesn't include any funds
```
