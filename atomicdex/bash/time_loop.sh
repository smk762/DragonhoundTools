#!/bin/bash
for (( ; ; ))
do
  date "+%H:%M:%S   %d/%m/%y"
  ./version.sh
  sleep 300
done

