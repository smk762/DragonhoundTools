#!/bin/bash
KMD_SRC=$HOME/komodo/src
source $KMD_SRC/pubkey.txt
if [[ -z ${1} ]]; then
	echo "use like: ./reindex.sh KMD"
else
	$KMD_SRC/listassetchainparams | while read coins; do
		params=$(echo $coins | grep ac_name=$1)
		if [[ ${#params} -gt 0 ]]; then
			echo "Stopping $1"
			${KMD_SRC}/komodo-cli -ac_name=${1} stop
			sleep 30
			echo "Reindexing $1"
			echo "${KMD_SRC}/komodod ${params} -pubkey=${pubkey} -reindex &"
			${KMD_SRC}/komodod ${params} -pubkey=${pubkey} -reindex &
		fi
	done
fi
