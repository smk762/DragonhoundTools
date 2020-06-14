#!/bin/bash
pkill -9 iguana
chips-cli stop
gamecredits-cli stop
einsteinium-cli stop
gincoin-cli stop
komodo-cli stop
cd ~/AYAv2/src
./aryacoin-cli stop
komodo-cli -ac_name=MCL stop