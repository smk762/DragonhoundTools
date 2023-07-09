#!/usr/bin/env python3
import os
import requests

# See https://github.com/DeckerSU/insight-api-komodo for more info

class InsightAPI:
    def __init__(self, baseurl, api_path="insight-api-komodo", api_key=None):
        self.api_key = api_key # Unused for now, but may be used in the future
        self.api_url = f"{baseurl}/{api_path}"

    def address(self, address):
        '''Get information about an address'''
        url = f"{self.api_url}/addr/{address}"
        response = requests.get(url)
        return response.json()

    def address_balance(self, address):
        '''Get the balance of an address in satoshis'''
        url = f'{self.api_url}/addr/{address}/balance'
        response = requests.get(url)
        return response.json()

    def address_transactions(self, address):
        '''Get the transactions for an address'''
        url = f"{self.api_url}/txs/?address={address}"
        response = requests.get(url)
        return response.json()

    def address_utxos(self, address):
        '''Get the unspent outputs for an address'''
        url = f'{self.api_url}/addr/{address}/balance'
        response = requests.get(url)
        return response.json()

    def addresses_transactions(self, addresses, from_=None, to_=None, no_asm=None, no_script_sig=None, no_spent=None):
        '''Get the transactions for multiple addresses'''
        url = f"{self.api_url}/addrs/{addresses}/txs"
        params = {}
        if from_ is not None:
            params["from"] = from_
        if to_ is not None:
            params["to"] = to_
        if no_asm is not None:
            params["noAsm"] = no_asm
        if no_script_sig is not None:
            params["noScriptSig"] = no_script_sig
        if no_spent is not None:
            params["noSpent"] = no_spent
        response = requests.get(url, params=params)
        return response.json()

    def blockhash_info(self, blockhash):
        '''Get information about a block with given block hash'''
        url = f'{self.api_url}/block/{blockhash}'
        response = requests.get(url)
        return response.json()

    def blockhash_transactions(self, block_hash):
        '''Get the transactions for a block with given block hash'''
        url = f"{self.api_url}/txs/?block={block_hash}"
        response = requests.get(url)
        return response.json()

    def blockindex_info(self, blockheight):
        '''Get information about a block with given block height'''
        url = f'{self.api_url}/block-index/{blockheight}'
        response = requests.get(url)
        return response.json()        

    def blocks_on_date(self, date, limit=None):
        '''Get block summaries by date'''
        
        if limit:
            url = f'{self.api_url}/blocks?blockDate={date}&limit={limit}'
        else:
            url = f'{self.api_url}/blocks?blockDate={date}'
        response = requests.get(url)
        return response.json()        

    def rawblock(self, blockheight=None, blockhash=None):
        '''Get raw block data for a block with given block height or hash'''
        if blockhash:
            url = f'{self.api_url}/rawblock/{blockhash}'
        else:
            blockhash = self.blockindex_info(blockheight)["blockHash"]
            url = f'{self.api_url}/rawblock/{blockheight}'
        response = requests.get(url)
        return response.json()

    def rawtransaction(self, txid):
        '''Get raw transaction data for a transaction with given transaction id'''
        url = f'{self.api_url}/rawtx/{txid}'
        response = requests.get(url)
        return response.json()
    
    def sync(self):
        '''Get the current sync status'''
        url = f'{self.api_url}/sync'
        response = requests.get(url)
        return response.json()
    
    def transaction(self, txid):
        '''Get information about a transaction with given transaction id'''
        url = f'{self.api_url}/tx/{txid}'
        response = requests.get(url)
        return response.json()
    
    def transaction_status(self, txid):
        '''Get the status of a transaction with given transaction id'''
        url = f'{self.api_url}/tx/{txid}/status'
        response = requests.get(url)
        return response.json()
    
    def transaction_utxos(self, txid):
        '''Get the unspent outputs for a transaction with given transaction id'''
        url = f'{self.api_url}/tx/{txid}/utxo'
        response = requests.get(url)
        return response.json()
    
    def transactions(self, txids):
        '''Get information about multiple transactions with given transaction ids'''
        url = f'{self.api_url}/txs/?txid={txids}'
        response = requests.get(url)
        return response.json()
    
    def transactions_block(self, blockhash):
        '''Get the transactions for a block with given block hash'''
        url = f'{self.api_url}/txs/?block={blockhash}'
        response = requests.get(url)
        return response.json()
    
    def transactions_block_height(self, blockheight):
        '''Get the transactions for a block with given block height'''
        blockhash = self.blockindex_info(blockheight)["blockHash"]
        url = f'{self.api_url}/txs/?block={blockhash}'
        response = requests.get(url)
        return response.json()
    
    def transactions_address(self, address):
        '''Get the transactions for an address'''
        url = f'{self.api_url}/txs/?address={address}'
        response = requests.get(url)
        return response.json()
    
    def transactions_addresses(self, addresses):
        '''Get the transactions for multiple addresses'''
        url = f'{self.api_url}/txs/?address={addresses}'
        response = requests.get(url)
        return response.json()


