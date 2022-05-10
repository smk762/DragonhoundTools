Here's a list of potentially useful commands which one of the notary nodes has mentioned in Discord:

Shortcut to importing key into other chain, rescanning from 10 blocks before current tip
`komodo-cli -ac_name=$chain importprivkey $(komodo-cli dumpprivkey $(komodo-cli listaddressgroupings|jq -r '.[][][0]')) "" true $(($(komodo-cli -ac_name=$chain getblockcount)-10))`
