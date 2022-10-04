#!/bin/bash

source userpass
curl --url "http://127.0.0.1:7783" --data "[
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"BCH\",\"servers\":[{\"url\":\"electrum1.cipig.net:10055\"},{\"url\":\"electrum2.cipig.net:10055\"}]},
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"KMD\",\"servers\":[{\"url\":\"electrum1.cipig.net:10001\"},{\"url\":\"electrum2.cipig.net:10001\"}]},
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"LTC\",\"servers\":[{\"url\":\"electrum-ltc.bysh.me:50001\"},{\"url\":\"electrum.ltc.xurious.com:50001\"}]},
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"MORTY\",\"servers\":[{\"url\":\"electrum1.cipig.net:10018\"},{\"url\":\"electrum2.cipig.net:10018\"}]},
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"RICK\",\"servers\":[{\"url\":\"electrum1.cipig.net:10017\"},{\"url\":\"electrum2.cipig.net:10017\"}]},
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"DASH\",\"servers\":[{\"url\":\"electrum1.cipig.net:10061\"},{\"url\":\"electrum2.cipig.net:10061\"}]},
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"DOGE\",\"servers\":[{\"url\":\"electrum1.cipig.net:10060\"},{\"url\":\"electrum2.cipig.net:10060\"}]},
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"DGB\",\"servers\":[{\"url\":\"electrum1.cipig.net:10059\"},{\"url\":\"electrum2.cipig.net:10059\"}]},
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"KOIN\",\"servers\":[{\"url\":\"electrum1.cipig.net:10024\"},{\"url\":\"electrum2.cipig.net:10024\"}]},
{\"userpass\":\"$userpass\",\"method\":\"electrum\",\"coin\":\"ZEC\",\"servers\":[{\"url\":\"electrum1.cipig.net:10058\"},{\"url\":\"electrum2.cipig.net:10058\"}]}
]"
