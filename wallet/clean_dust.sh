#!/bin/bash
SHELL=/bin/sh PATH=/bin:/sbin:/usr/bin:/usr/sbin
 
#Use like:  ./clean_dust.sh BEER R-addr 
ac_name=${1}
Radd="${2}"


if [ "${1}" != "KMD" ] && [ "${1}" != "" ]; then
    AssetChain=" -ac_name="${1}
else
    AssetChain=""
fi

function makeRaw() {
    for ((tc = 0; tc <= $1 - 1; tc++)); do
        RawOut2="{\"txid\":\"${txids[tc]}\",\"vout\":${vouts[tc]}},"
        RawOut="$RawOut$RawOut2"
        OutAmount=$(echo "scale=8; ($OutAmount + ${amounts[tc]})" | bc)
    done
    OutAmount=$(echo "scale=8; $OutAmount - 0.00000001" | bc) OutAmount=${OutAmount/#./0.}
    RawOut="${RawOut::-1}" RawOut=$RawOut"] {\"$Radd\":$OutAmount}"
    echo $RawOut
}
function addnlocktime() {
    nlocktime=$(printf "%08x" $(date +%s) | dd conv=swab 2>/dev/null | rev)
    chophex=$(echo $toSign | sed 's/.\{38\}$//')
    nExpiryHeight=$(echo $toSign | grep -o '.\{30\}$')
    newhex=$chophex$nlocktime$nExpiryHeight
}


function cook_utxos() {
    maxInc="1300" MinCheck="1" RawOut="[" OutAmount="0"
    maxconf="1"
    txids=() vouts=() amounts=()
    echo "Finding UTXOS in $maxconf blocks to consolidate ..."
    unspents=$(./komodo-cli${AssetChain} listunspent $MinCheck 120000)
#echo $unspents
    inputUTXOs=$(jq -cr '[map(select((.spendable == true) and (.rawconfirmations >= 1) and (.interest != 0.00000000))) | .[] | {txid, vout, amount}]' <<<"${unspents}")
# echo $inputUTXOs
    for txid in $(jq -r '.[].txid' <<<"${inputUTXOs}"); do
	echo $txid
	txids+=("$txid"); 
    done

    for vout in $(jq -r '.[].vout' <<<"${inputUTXOs}"); do vouts+=("$vout"); done
echo $vouts
    for amount in $(jq -r '.[].amount' <<<"${inputUTXOs}"); do
        if [[ "$amount" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
            amounts+=("$amount")
        else
            amounts+=("$(printf "%.8f" $amount)")
        fi
    done
    echo  ${vouts[@]}
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
    echo "$OutAmount ${ac_name} sent to $Radd"
}
cd ~/komodo/src
unspent_utxos=$(./komodo-cli${AssetChain} listunspent | jq length)
echo "========= $unspent_utxos utxos remaining =========="
while [ ${unspent_utxos} -gt 100 ]; do
    cook_utxos
    unspent_utxos=$(./komodo-cli${AssetChain} listunspent | jq length)
    echo "========= $unspent_utxos utxos remaining =========="
done

