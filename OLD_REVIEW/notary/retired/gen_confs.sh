#!/bin/bash

mkdir ~/.chips
cp ../config/conf.template ~/.chips/chips.conf
user=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64)
pass=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64)
sed -i 's/a_secure_user/'$user'/g' ~/.chips/chips.conf
sed -i 's/a_secure_password/'$user'/g' ~/.chips/chips.conf

mkdir ~/.gamecredits
cp ../config/conf.template ~/.gamecredits/gamecredits.conf
user=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64)
pass=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64)
sed -i 's/a_secure_user/'$user'/g' ~/.gamecredits/gamecredits.conf
sed -i 's/a_secure_password/'$user'/g' ~/.gamecredits/gamecredits.conf


mkdir ~/.einsteinium
cp ../config/conf.template ~/.einsteinium/einsteinium.conf
user=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64)
pass=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64)
sed -i 's/a_secure_user/'$user'/g' ~/.einsteinium/einsteinium.conf
sed -i 's/a_secure_password/'$user'/g' ~/.einsteinium/einsteinium.conf

mkdir ~/.gincoincore
cp ../config/conf.template ~/.gincoincore/gincoin.conf
user=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64)
pass=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64)
sed -i 's/a_secure_user/'$user'/g' ~/.gincoincore/gincoin.conf
sed -i 's/a_secure_password/'$user'/g' ~/.gincoincore/gincoin.conf

mkdir ~/.komodo3
touch ~/.komodo3/komodo.conf
echo "rpcuser="$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64) >> ~/.komodo3/komodo.conf
echo "rpcpassword="$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c64) >> ~/.komodo3/komodo.conf
echo "txindex=1" >> ~/.komodo3/komodo.conf
echo "server=1" >> ~/.komodo3/komodo.conf
echo "daemon=1" >> ~/.komodo3/komodo.conf
echo "rpcport=7620" >> ~/.komodo3/komodo.conf
echo "p2pport=7621" >> ~/.komodo3/komodo.conf
echo "rpcworkqueue=256" >> ~/.komodo3/komodo.conf
echo "rpcbind=127.0.0.1" >> ~/.komodo3/komodo.conf
echo "rpcallowip=127.0.0.1" >> ~/.komodo3/komodo.conf
