#!/bin/bash
./listclis.sh | while read coin; do
  echo $coin
len="$($coin listreceivedbyaddress | jq '.[].txids' | jq length)"
echo "$len"
if (($len > 30));
then
  $coin cleanwallettransactions
fi
done
