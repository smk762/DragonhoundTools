#!/bin/bash
source userpass

# Enable coins

# IRIS
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable_tendermint_with_assets\",\"mmrpc\":\"2.0\",\"params\":{\"ticker\":\"IRIS_TEST\",\"tokens_params\":[{\"ticker\":\"IRIS_NIMDA_TEST\"},{\"ticker\":\"USDC_IBC_IRIS_TEST\"}], \"rpc_urls\":[\"http://34.80.202.172:26657\"]},\"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable_tendermint_with_assets\",\"mmrpc\":\"2.0\",\"params\":{\"ticker\":\"IRIS\",     \"tokens_params\":[{\"ticker\":\"ATOM-IBC_IRIS\"}],\"rpc_urls\":[\"https://iris.komodo.live/\"]},\"userpass\":\"$userpass\"}"; echo

# AVX20
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"AVAXT\",      \"swap_contract_address\":\"0x9130b257D37A52E52F21054c4DA3450c72f595CE\",\"fallback_swap_contract\":\"0x9bC5418CEdED51dB08467fc4b62F32C5D9EBdA55\",\"urls\":[\"https://api.avax.network/ext/bc/C/rpc\"],\"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"AVAX\",       \"swap_contract_address\":\"0x9130b257D37A52E52F21054c4DA3450c72f595CE\",\"fallback_swap_contract\":\"0x9bC5418CEdED51dB08467fc4b62F32C5D9EBdA55\",\"urls\":[\"https://api.avax.network/ext/bc/C/rpc\"],\"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"USDC-AVX20\", \"swap_contract_address\":\"0x9130b257D37A52E52F21054c4DA3450c72f595CE\",\"fallback_swap_contract\":\"0x9bC5418CEdED51dB08467fc4b62F32C5D9EBdA55\",\"urls\":[\"https://api.avax.network/ext/bc/C/rpc\"],\"userpass\":\"$userpass\"}"; echo

# BEP20
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"BNBT\",       \"swap_contract_address\":\"0xB1Ad803ea4F57401639c123000C75F5B66E4D123\",\"fallback_swap_contract\":\"0xcCD17C913aD7b772755Ad4F0BDFF7B34C6339150\",\"urls\":[\"https://data-seed-prebsc-1-s2.binance.org:8545\"], \"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"BNB\",        \"swap_contract_address\":\"0x5404A1F32C28fE2ee1819344a459c37fA8aC1f8F\",\"fallback_swap_contract\":\"0xeDc5b89Fe1f0382F9E4316069971D90a0951DB31\",\"urls\":[\"https://bold-silent-silence.bsc.quiknode.pro/051a7ab8bacba41205fe5a278bd75a4249e4ac11/\",\"http://bsc1.cipig.net:8655\", \"http://bsc2.cipig.net:8655\", \"http://bsc3.cipig.net:8655\"], \"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"USDC-BEP20\", \"swap_contract_address\":\"0x5404A1F32C28fE2ee1819344a459c37fA8aC1f8F\",\"fallback_swap_contract\":\"0xeDc5b89Fe1f0382F9E4316069971D90a0951DB31\",\"urls\":[\"https://bold-silent-silence.bsc.quiknode.pro/051a7ab8bacba41205fe5a278bd75a4249e4ac11/\",\"http://bsc1.cipig.net:8655\", \"http://bsc2.cipig.net:8655\", \"http://bsc3.cipig.net:8655\"], \"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"KMD-BEP20\",  \"swap_contract_address\":\"0x5404A1F32C28fE2ee1819344a459c37fA8aC1f8F\",\"fallback_swap_contract\":\"0xeDc5b89Fe1f0382F9E4316069971D90a0951DB31\",\"urls\":[\"https://bold-silent-silence.bsc.quiknode.pro/051a7ab8bacba41205fe5a278bd75a4249e4ac11/\",\"http://bsc1.cipig.net:8655\", \"http://bsc2.cipig.net:8655\", \"http://bsc3.cipig.net:8655\"], \"userpass\":\"$userpass\"}"; echo

# ERC20
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"ETH\",        \"swap_contract_address\":\"0x34CB0da0ED7005870D28e41983F934D7205fC360\", \"fallback_swap_contract\":\"0x24ABE4c71FC658C91313b6552cd40cD808b3Ea80\",\"urls\":[\"https://rpc.ankr.com/eth\",\"https://api.mycryptoapi.com/eth\",\"https://eth-mainnet.nodereal.io/v1/1659dfb40aa24bbb8153a677b98064d7\",\"https://rpc.flashbots.net\"],\"gas_station_url\":\"https://ethgasstation.info/json/ethgasAPI.json\", \"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"USDC-ERC20\", \"swap_contract_address\":\"0x34CB0da0ED7005870D28e41983F934D7205fC360\", \"fallback_swap_contract\":\"0x24ABE4c71FC658C91313b6552cd40cD808b3Ea80\",\"urls\":[\"https://rpc.ankr.com/eth\",\"https://api.mycryptoapi.com/eth\",\"https://eth-mainnet.nodereal.io/v1/1659dfb40aa24bbb8153a677b98064d7\",\"https://rpc.flashbots.net\"],\"gas_station_url\":\"https://ethgasstation.info/json/ethgasAPI.json\", \"userpass\":\"$userpass\"}"; echo

# PLG20
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"MATICTEST\",  \"swap_contract_address\":\"0x73c1Dd989218c3A154C71Fc08Eb55A24Bd2B3A10\",\"fallback_swap_contract\":\"0x73c1Dd989218c3A154C71Fc08Eb55A24Bd2B3A10\",\"urls\":[\"https://rpc-mumbai.matic.today\",\"https://matic-mumbai.chainstacklabs.com\",\"https://rpc-mumbai.maticvigil.com\"], \"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"MATIC\",      \"swap_contract_address\":\"0x9bC5418CEdED51dB08467fc4b62F32C5D9EBdA55\",\"fallback_swap_contract\":\"0x9130b257D37A52E52F21054c4DA3450c72f595CE\",\"urls\":[\"https://winter-hidden-haze.matic.quiknode.pro/67032dcaae92eccfa89a06596cc85b123b3c0aae/\",\"https://polygon-rpc.com\"], \"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"enable\",\"coin\":\"USDC-PLG20\", \"swap_contract_address\":\"0x9bC5418CEdED51dB08467fc4b62F32C5D9EBdA55\",\"fallback_swap_contract\":\"0x9130b257D37A52E52F21054c4DA3450c72f595CE\",\"urls\":[\"https://winter-hidden-haze.matic.quiknode.pro/67032dcaae92eccfa89a06596cc85b123b3c0aae/\",\"https://polygon-rpc.com\"], \"userpass\":\"$userpass\"}"; echo

# UTXO
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"electrum\",\"coin\":\"KMD\",   \"servers\":[{\"url\":\"electrum1.cipig.net:10001\"},{\"url\":\"electrum2.cipig.net:10001\"},{\"url\":\"electrum3.cipig.net:10001\"}],\"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"electrum\",\"coin\":\"RICK\",  \"servers\":[{\"url\":\"electrum1.cipig.net:10017\"},{\"url\":\"electrum2.cipig.net:10017\"},{\"url\":\"electrum3.cipig.net:10017\"}],\"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"electrum\",\"coin\":\"MORTY\", \"servers\":[{\"url\":\"electrum1.cipig.net:10018\"},{\"url\":\"electrum2.cipig.net:10018\"},{\"url\":\"electrum3.cipig.net:10018\"}],\"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"electrum\",\"coin\":\"DGB\",   \"servers\":[{\"url\":\"electrum1.cipig.net:10059\"},{\"url\":\"electrum2.cipig.net:10059\"},{\"url\":\"electrum3.cipig.net:10059\"}],\"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"electrum\",\"coin\":\"DOGE\",  \"servers\":[{\"url\":\"electrum1.cipig.net:10060\"},{\"url\":\"electrum2.cipig.net:10060\"},{\"url\":\"electrum3.cipig.net:10060\"}],\"userpass\":\"$userpass\"}"; echo
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"electrum\",\"coin\":\"LTC\",   \"servers\":[{\"url\":\"electrum1.cipig.net:10063\"},{\"url\":\"electrum2.cipig.net:10063\"},{\"url\":\"electrum3.cipig.net:10063\"}],\"userpass\":\"$userpass\"}"; echo
sleep 3







# Start Bot
curl --url 'http://127.0.0.1:7783' --data "{
    \"userpass\": \"${userpass}\",
    \"mmrpc\": \"2.0\",
    \"method\": \"start_simple_market_maker_bot\",
    \"params\": {
        \"price_url\": \"https://prices.komodo.live:1313/api/v2/tickers?expire_at=600\",
        \"bot_refresh_rate\": 60,
        \"cfg\": {
            \"ATOM-IBC_IRIS/KMD\": {
                \"base\": \"ATOM-IBC_IRIS\",
                \"rel\": \"KMD\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"ATOM-IBC_IRIS/BNB\": {
                \"base\": \"ATOM-IBC_IRIS\",
                \"rel\": \"BNB\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"ATOM-IBC_IRIS/USDC-BEP20\": {
                \"base\": \"ATOM-IBC_IRIS\",
                \"rel\": \"USDC-BEP20\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"ATOM-IBC_IRIS/USDC-PLG20\": {
                \"base\": \"ATOM-IBC_IRIS\",
                \"rel\": \"USDC-PLG20\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"KMD/ATOM-IBC_IRIS\": {
                \"rel\": \"ATOM-IBC_IRIS\",
                \"base\": \"KMD\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"BNB/ATOM-IBC_IRIS\": {
                \"rel\": \"ATOM-IBC_IRIS\",
                \"base\": \"BNB\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"USDC-BEP20/ATOM-IBC_IRIS\": {
                \"rel\": \"ATOM-IBC_IRIS\",
                \"base\": \"USDC-BEP20\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"USDC-PLG20/ATOM-IBC_IRIS\": {
                \"rel\": \"ATOM-IBC_IRIS\",
                \"base\": \"USDC-PLG20\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },            
            \"IRIS/KMD\": {
                \"base\": \"IRIS\",
                \"rel\": \"KMD\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"IRIS/BNB\": {
                \"base\": \"IRIS\",
                \"rel\": \"BNB\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"IRIS/USDC-BEP20\": {
                \"base\": \"IRIS\",
                \"rel\": \"USDC-BEP20\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"IRIS/USDC-PLG20\": {
                \"base\": \"IRIS\",
                \"rel\": \"USDC-PLG20\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"KMD/IRIS\": {
                \"rel\": \"IRIS\",
                \"base\": \"KMD\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"BNB/IRIS\": {
                \"rel\": \"IRIS\",
                \"base\": \"BNB\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"USDC-BEP20/IRIS\": {
                \"rel\": \"IRIS\",
                \"base\": \"USDC-BEP20\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            },
            \"USDC-PLG20/IRIS\": {
                \"rel\": \"IRIS\",
                \"base\": \"USDC-PLG20\",
                \"max\": true,
                \"spread\": \"1.01\",
                \"base_confs\": 3,
                \"base_nota\": false,
                \"rel_confs\": 3,
                \"rel_nota\": false,
                \"enable\": true,
                \"price_elapsed_validity\": 60.0
            }
        }
    },
    \"id\": 0
}"
echo
