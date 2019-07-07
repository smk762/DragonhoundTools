#!/bin/bash
SHELL=/bin/sh PATH=/bin:/sbin:/usr/bin:/usr/sbin

cd $HOME/komodo/src #komodo-cli location
 
#Use like:  ./clean_dust.sh BEER 
 
# Replace address below with destination address 
Addy="RRfUCLxfT5NMpxsC9GHVbdfVy5WJnJFQLV"

AssetChain=""
if [ "${1}" != "KMD" ] && [ "${1}" != "" ]; then
AssetChain=" -ac_name="${1}
fi
ac_name=${1}
function makeRaw() {
    for ((tc = 0; tc <= $1 - 1; tc++)); do
        RawOut2="{\"txid\":\"${txids[tc]}\",\"vout\":${vouts[tc]}},"
        RawOut="$RawOut$RawOut2"
        OutAmount=$(echo "scale=8; ($OutAmount + ${amounts[tc]})" | bc)
    done
    OutAmount=$(echo "scale=8; $OutAmount - 0.00000001" | bc) OutAmount=${OutAmount/#./0.}
    RawOut="${RawOut::-1}" RawOut=$RawOut"] {\"$Addy\":$OutAmount}"
}
function addnlocktime() {
    nlocktime=$(printf "%08x" $(date +%s) | dd conv=swab 2>/dev/null | rev)
    chophex=$(echo $toSign | sed 's/.\{38\}$//')
    nExpiryHeight=$(echo $toSign | grep -o '.\{30\}$')
    newhex=$chophex$nlocktime$nExpiryHeight
}


function cook_utxos() {
    maxInc="1300" MinCheck="1" RawOut="[" OutAmount="0"
    maxconf="500000000000"
    txids=() vouts=() amounts=()
    echo "Finding UTXOS in $maxconf blocks to consolidate ..."
    unspents=$(./komodo-cli${AssetChain} listunspent $MinCheck 120000)
    inputUTXOs=$(jq -cr '[map(select((.spendable == true) and (.rawconfirmations >= 1) and (.interest != 0.00000000))) | .[] | {txid, vout, amount}]' <<<"${unspents}")
    for txid in $(jq -r '.[].txid' <<<"${inputUTXOs}"); do txids+=("$txid"); done
    for vout in $(jq -r '.[].vout' <<<"${inputUTXOs}"); do vouts+=("$vout"); done
    for amount in $(jq -r '.[].amount' <<<"${inputUTXOs}"); do
        if [[ "$amount" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
            amounts+=("$amount")
        else
            amounts+=("$(printf "%.8f" $amount)")
        fi
    done
    if [[ ${#vouts[@]} -ge $maxInc ]]; then
        makeRaw $maxInc
    else
        makeRaw ${#vouts[@]}
    fi
    toSign=$(./komodo-cli${AssetChain} createrawtransaction $RawOut)
    addnlocktime
    Signed=$(./komodo-cli${AssetChain} signrawtransaction $newhex | jq -r '.hex')
    lasttx=$(echo -e "$Signed" | ./komodo-cli${AssetChain} -stdin sendrawtransaction)
    echo "Sent signed raw consolidated tx: $lasttx"
    echo "$OutAmount ${ac_name} sent to $Addy"
}

unspent_utxos=$(./komodo-cli${AssetChain} listunspent | jq length)
echo "========= $unspent_utxos utxos remaining =========="
while [ ${unspent_utxos} -gt 100 ]; do
    cook_utxos
    unspent_utxos=$(./komodo-cli${AssetChain} listunspent | jq length)
    echo "========= $unspent_utxos utxos remaining =========="
done

