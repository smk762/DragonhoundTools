#!/bin/bash
cd "${BASH_SOURCE%/*}" || exit
# Local split version by webworker01
# Adapted for testnet by SHossain
# Original version by Decker (c) 2018 <https://github.com/DeckerSU/komodo_scripts/blob/master/split_nn_sapling.sh>
#
# Requires package dc, bc, & jq - sudo apt-get install dc bc jq
# 
# Enter your address in line 16
# provide location of your `komodo-cli` binary in line 21
#
# Usage: ./splitfunds <COINNAME> <numutxos> <sapling=1/0>
# e.g.   ./splitfunds KMD 50
# e.g.   ./splitfunds OOT 50 0

NN_ADDRESS=RUfGdUVjvwC1ivquiN43Fu8aXJ6pCjkirp
txfee=0.0001

# fetch this coins cli path
if [[ ! -z $1 ]]; then
    cli=/home/$USER/komodo/src/komodo-cli
fi

#Do not change below for any reason!

#base58 decode by grondilu https://github.com/grondilu/bitcoin-bash-tools/blob/master/bitcoin.sh
declare -a base58=(
      1 2 3 4 5 6 7 8 9
    A B C D E F G H   J K L M N   P Q R S T U V W X Y Z
    a b c d e f g h i j k   m n o p q r s t u v w x y z
)
unset dcr; for i in {0..57}; do dcr+="${i}s${base58[i]}"; done
decodeBase58() {
    local line
    echo -n "$1" | sed -e's/^\(1*\).*/\1/' -e's/1/00/g' | tr -d '\n'
    dc -e "$dcr 16o0$(sed 's/./ 58*l&+/g' <<<$1)p" |
    while read line; do echo -n ${line/\\/}; done
}


SPLIT_COUNT=$2
#Splits > 252 are not allowed
if [[ ! -z $SPLIT_COUNT ]] && (( SPLIT_COUNT > 252 )); then
    SPLIT_COUNT=252
elif [[ ! -z $SPLIT_COUNT ]] && (( SPLIT_COUNT > 0 )); then
    SPLIT_COUNT=$2
else
    #it wasn't a number, default to 50
    SPLIT_COUNT=50
fi

if [[ ! -z $3 ]] && [[ $3 != "1" ]]; then
    sapling=0
else
    sapling=1
fi

SPLIT_VALUE=0.0001
SPLIT_VALUE_SATOSHI=10000
# add a 10k sat txfee for KMD. 
SPLIT_TOTAL=$(jq -n --arg txfee $txfee "$SPLIT_VALUE*($SPLIT_COUNT+$txfee)")

NN_PUBKEY=$(${cli} validateaddress $NN_ADDRESS | jq -r .pubkey)
nob58=$(decodeBase58 $NN_ADDRESS)
NN_HASH160=$(echo ${nob58:2:-8})

#Get lowest amount and valid utxo to split |||| (and .generated==false) this isnt a real limitation. 
utxo=$(${cli} listunspent | jq -r --arg minsize $SPLIT_TOTAL '[.[] | select(.amount>($minsize|tonumber) and .rawconfirmations>0)] | sort_by(.amount)[0]')

if [[ $utxo != "null" ]]; then
    
    txid=$(jq -r .txid <<< $utxo)
    vout=$(jq -r .vout <<< $utxo)
    amount=$(jq -r .amount <<< $utxo)

    rev_txid=$(dd conv=swab 2>/dev/null <<< $txid | rev)
    vout_hex=$(printf "%08x" $vout | dd conv=swab 2>/dev/null | rev)

    if (( sapling > 0 )); then
        rawtx="04000080" # tx version
        rawtx=$rawtx"85202f89" # versiongroupid
    else
        rawtx="01000000" # tx version
    fi

    rawtx=$rawtx"01" # number of inputs (1, as we take one utxo from listunspent)
    rawtx=$rawtx$rev_txid$vout_hex"00ffffffff"

    outputCount=$(printf "%02x" $((SPLIT_COUNT+1)) )
    rawtx=$rawtx$outputCount

    value=$(printf "%016x" $SPLIT_VALUE_SATOSHI | dd conv=swab 2>/dev/null | rev)
    outbits=$value"2321"$NN_PUBKEY"ac"
    outbits=$(eval printf "%0.s$outbits" {1..$SPLIT_COUNT})
    rawtx=$rawtx$outbits

    change=$( printf "%.8f" $(bc -l <<< "($amount-$SPLIT_TOTAL)") )
    change=$( sed 's/^0*//' <<< ${change//./} )
    change=$( printf "%016x" $change | dd conv=swab 2> /dev/null | rev )
    rawtx=$rawtx$change

    rawtx=$rawtx"1976a914"$NN_HASH160"88ac" # len OP_DUP OP_HASH160 len hash OP_EQUALVERIFY OP_CHECKSIG

    nlocktime="00000000"
    rawtx=$rawtx$nlocktime

    if (( sapling > 0 )); then
        rawtx=$rawtx"000000000000000000000000000000" # sapling end of tx
    fi

    signedtx=$(${cli} signrawtransaction $rawtx | jq -r '.hex')

    if [[ ! -z $signedtx ]]; then
        txid=$(${cli} sendrawtransaction $signedtx)
        echo '{"txid":"'"$txid"'"}'
    else
        echo '{"error":"failed to sign tx"}'
    fi
else
  echo '{"error":"No UTXOs to split :(("}'
fi
