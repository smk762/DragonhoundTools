#!/bin/bash
# Suggest using with this command: watch --color -n 60 ./status
# From https://github.com/chainstrike/nntools/blob/master/status.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
printf "Notary Node Status\n"
printf "==================\n"



function show_walletsize () {
  if [ "$1" != "KMD" ] && [ "$1" != "BTC" ]; then
    if [ -f ~/.komodo/$1/wallet.dat ]; then
      # SIZE=$(stat ~/.komodo/$1/wallet.dat | grep -Po "Size: \d*" | cut -d" " -f2)
      # Pattern "Size: " - is only for english locale, so, we won't use it.

      SIZE=$(stat ~/.komodo/$1/wallet.dat | grep -Po "\d+" | head -1)
    else
      SIZE=0
    fi
  elif [ "$1" = "BTC" ]; then
    SIZE=$(stat ~/.bitcoin/wallet.dat | grep -Po "\d+" | head -1)
  elif [ "$1" = "KMD" ]; then
    SIZE=$(stat ~/.komodo/wallet.dat | grep -Po "\d+" | head -1)
  fi

  OUTSTR=$(echo $SIZE | numfmt --to=si --suffix=B)

  if [ "$SIZE" -gt "19222944" ]; then
    OUTSTR=${RED}$OUTSTR${RESET}
  else
    OUTSTR=${GREEN}$OUTSTR${RESET}
  fi

  printf "%16b\n" $OUTSTR

}



function process_check () {
  ps_out=`ps -ef | grep $1 | grep -v 'grep' | grep -v $0`
  result=$(echo $ps_out | grep "$1")
 if [[ "$result" != "" ]];then
    echo "here"
    return 1
  else
    echo "other"
    return 0
fi
}

UP="$(/usr/bin/uptime)"

echo "Server Uptime: $UP"
#TO DO
#ADD UPTIME CHECK
#ADD LOW BALANCE CHECK
#ADD LOW CPU USAGE CHECK

processlist=(
'iguana'
'komodod'
'PIZZA'
'TXSCLCC'
'BEER'
)

count=0
while [ "x${processlist[count]}" != "x" ]
do
  echo -n "${processlist[count]}"
  #fixes formating issues
  size=${#processlist[count]}
  if [ "$size" -lt "8" ]
  then
    echo -n -e "\t\t"
  else
    echo -n -e "\t"
  fi
  if [ $(process_check $processlist[count]) ]
  then
    printf "Process: ${GREEN} Running ${NC}"
    if [ "$count" = "1" ]
    then
            cd ~/komodo/src
            RESULT="$(./komodo-cli -rpcclienttimeout=15 listunspent | grep .00010000 | wc -l)"
            RESULT1="$(./komodo-cli -rpcclienttimeout=15  listunspent|grep amount|awk '{print $2}'|sed s/.$//|awk '$1 < 0.0001'|wc -l)"
            RESULT2="$(./komodo-cli -rpcclienttimeout=15 getbalance)"
            RESULT3="$(./komodo-cli -rpcclienttimeout=15 getwalletinfo | jq '.txcount')"
            RESULT4="$(show_walletsize KMD)"


    fi
    if [ "$count" -gt "1" ]
    then
            cd ~/komodo/src
            RESULT="$(./komodo-cli -rpcclienttimeout=15 -ac_name=${processlist[count]} listunspent | grep .00010000 | wc -l)"
            RESULT1="$(./komodo-cli -ac_name=${processlist[count]} -rpcclienttimeout=15  listunspent|grep amount|awk '{print $2}'|sed s/.$//|awk '$1 < 0.0001'|wc -l)"
            RESULT2="$(./komodo-cli -rpcclienttimeout=15 -ac_name=${processlist[count]} getbalance)"
            RESULT3="$(./komodo-cli -rpcclienttimeout=15 -ac_name=${processlist[count]} getwalletinfo | jq '.txcount')"
	    RESULT4="$(show_walletsize ${processlist[count]})"
    fi
# Check if we have actual results next two lines check for valid number.
if [[ $RESULT == ?([-+])+([0-9])?(.*([0-9])) ]] ||
       [[ $RESULT == ?(?([-+])*([0-9])).+([0-9]) ]]
    then
    if [ "$RESULT" -lt "30" ]
    then
    printf  "| Avail UTXOs: ${RED}$RESULT\t${NC}"
    else
    printf  "| Avail UTXOs: ${GREEN}$RESULT\t${NC}"
    fi
fi

 if [[ $RESULT1 == ?([-+])+([0-9])?(.*([0-9])) ]] ||
       [[ $RESULT1 == ?(?([-+])*([0-9])).+([0-9]) ]]
    then
    if [ "$RESULT1" -gt "0" ]
    then
    printf  "| Dust UTXOs: ${RED}$RESULT1\t${NC}"
    else
    printf  "| Dust UTXOs: ${GREEN}$RESULT1\t${NC}"
    fi
fi


if [[ $RESULT2 == ?([-+])+([0-9])?(.*([0-9])) ]] ||
    [[ $RESULT2 == ?(?([-+])*([0-9])).+([0-9]) ]]
    then
    if (( $(echo "$RESULT2 > 0.1" | bc -l) ));
    then
    printf  "| Avail Funds: ${GREEN}$RESULT2\t${NC}"

    else
    printf  "| Avail Funds: ${RED}$RESULT2\t${NC}"
    fi
fi
if [[ $RESULT3 == ?([-+])+([0-9])?(.*([0-9])) ]] ||
    [[ $RESULT3 == ?(?([-+])*([0-9])).+([0-9]) ]]
    then
    if (( $(echo "$RESULT3 > 100" | bc -l) ));
    then
    printf  "| TX Count: ${RED}$RESULT3\t${NC}"

    else
    printf  "| TX Count: ${GREEN}$RESULT3\t${NC}"
   fi
fi
    printf  "| Wallet Size: ${RED}$RESULT4\t${NC}\n"

    RESULT=""
    RESULT2=""
    RESULT3=""
    RESULT4=""

  else
    printf "Process: ${RED} Not Running ${NC}\n"
    echo "Not Running"
  fi
  count=$(( $count +1 ))
done
