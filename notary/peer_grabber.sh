#!/bin/bash

# Credit: CG https://discord.com/channels/412898016371015680/455755767132454913/1124371545800839238

SHELL=/bin/sh PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
coins="KMD CHIPS MCL TOKEL VRSC AYA EMC2 MIL"
coins_info='{"CHIPS":{"daemon":"chipsd","client":"chips-cli"},"AYA":{"daemon":"aryacoind","client":"aryacoin-cli"},"EMC2":{"daemon":"einsteiniumd","client":"einsteinium-cli"},"MIL":{"daemon":"mild","client":"mil-cli"}}'
for j in $(curl -s --url "http://127.0.0.1:7779/" --data "{\"agent\":\"dpow\",\"method\":\"ipaddrs\"}" | jq -r .[]); do
    for coin in ${coins}; do
                echo "Adding ${j} to ${coin}"
        case "${coin}" in
            "KMD")
                coin_client="komodo-cli"
                ${coin_client} addnode ${j} onetry
                ;;
            "TOKEL" | "MCL" | "VRSC")
                coin_client="komodo-cli -ac_name=${coin}"
                ${coin_client} addnode ${j} onetry
                ;;
            *)
                coin_info=$(jq --arg key2 "${coin}" '.[$key2]' <<<"${coins_info}")
                coin_client=$(jq -r '.client' <<<"${coin_info}")
                ${coin_client} addnode ${j} onetry
                ;;
        esac
    done
done
