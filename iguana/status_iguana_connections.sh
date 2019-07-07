#!/bin/bash

#from https://github.com/chainstrike/nntools/blob/master/ipcheck.sh
iguana_port='7776'
myip=$(curl -s4 checkip.amazonaws.com)

establishedconnections=$( ss -a | grep ":$iguana_port" | grep "ESTAB" | awk '{print $5 " "  $6}' )

#echo $"$establishedconnections"
outgoing=$( echo $"$establishedconnections" | grep -v "$myip:$iguana_port" | awk '{print $2}' | sed 's/:[0-9]*[0-9]*[0-9]*[0-9]//g' | sort  )
#echo $"$outgoing"
ingoing=$( echo $"$establishedconnections" | grep "$myip:$iguana_port" | awk '{print $2}' | sed 's/:[0-9]*[0-9]*[0-9]*[0-9]*//g' | sort  )
#echo $"$ingoing"


echo "# outgoing:"
echo $"$outgoing" | wc -l
echo ""
echo "# ingoing:"
echo $"$ingoing" | wc -l
echo ""
echo "IPs not ingoing:"
comm -23 <(echo "$outgoing") <(echo "$ingoing")
echo ""
echo "IPs not outgoing:"
comm -23 <(echo "$ingoing") <(echo "$outgoing")
