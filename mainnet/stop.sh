#!/bin/bash
komodo-cli stop
bitcoin-cli stop
#komodo-cli -ac_name=HUSH3 stop
cd ~/komodo/src
./fiat-cli stop
smk762@kmdNN:~/DragonhoundTools/notary$ cat NN_start.sh