#!/bin/bash

if [[ -z ${1} ]]; then
	echo "use like: ./add_whiteRadd.sh R-address"
else
	valid=$(komodo-cli validateaddress ${1} | jq .isvalid)
	if [[ "$valid" = "true" ]]; then
		echo "${1} whitelisted for all assetchains"
		find ~/.komodo -type f -iname "*.conf" -exec sh -c 'echo whitelistaddress='${1}' >> {}' \;
	else
		echo "${1} is not a valid R-address"
	fi
fi

