#!/bin/bash

source userpass
curl --url "http://127.0.0.1:7783" --data "[
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"RICK\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"KMD\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"LTC\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"MORTY\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"DASH\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"DOGE\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"DGB\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"KOIN\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"ZEC\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"BCH\",\"rel\":\"RICK\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"KMD\",\"rel\":\"BCH\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"KMD\",\"rel\":\"LTC\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"KMD\",\"rel\":\"MORTY\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"KMD\",\"rel\":\"DASH\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"KMD\",\"rel\":\"DOGE\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"KMD\",\"rel\":\"DGB\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"KMD\",\"rel\":\"KOIN\"},
{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"KMD\",\"rel\":\"ZEC\"}
]"
