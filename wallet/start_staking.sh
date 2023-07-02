#!/bin/bash
SHELL=/bin/sh PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin

komodo-cli -ac_name=${1} setgenerate true 0
komodo-cli -ac_name=${1} getgenerate
