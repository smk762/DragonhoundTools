#!/usr/bin/env python3

# DO WHAT THE F*** YOU WANT TO PUBLIC LICENSE  
#                   Version 2, December 2004  
#  
# Copyright (C) Dragonhound
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#      DO WHAT THE F*** YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE F*** YOU WANT TO.

import ssl
import json
import socket
import hashlib
import binascii
from base58 import b58decode_check
from lib_logger import logger


class ElectrumConnection():
    def __init__(self, url, port, ssl=False, timeout=30):
        self.url = url
        self.port = port
        self.ssl = ssl
        socket.setdefaulttimeout(timeout)
        # Initialize the connection
        self.version()

    def rpc(self, method, params=[]):
        params = [params] if not isinstance(params, list) else params
        if self.ssl:
            context = ssl.create_default_context()
            try:
                with socket.create_connection((url, port)) as sock:
                    with context.wrap_socket(sock, server_hostname=url) as ssock:
                        ssock.send(json.dumps({"id": 0, "method": method, "params": params}).encode() + b'\n')
                        return json.loads(ssock.recv(99999)[:-1].decode())
            except Exception as e:
                return e
        else:
            with socket.create_connection((url, port)) as sock:
                sock.send(json.dumps({"id": 0, "method": method, "params": params}).encode() + b'\n')
                return json.loads(sock.recv(99999)[:-1].decode())

    def version(self):
        return self.rpc("server.version")

    def broadcast(raw_tx):
        return self.rpc('blockchain.transaction.broadcast', raw_tx)

    def address_balance(address):
        return self.get_full_balance(address, pubkey=address)

    def pubkey_balance(pubkey):
        return self.get_full_balance(rpc, pubkey=pubkey)

    def lil_endian(hex_str):
        return ''.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)][::-1])

    def get_full_balance(rpc, address=None, pubkey=None):
        p2pkh_confirmed_balance = 0
        p2pkh_unconfirmed_balance = 0
        p2pk_confirmed_balance = 0
        p2pk_unconfirmed_balance = 0
        if pubkey:
            p2pk_scripthash = get_p2pk_scripthash_from_pubkey(pubkey)
            p2pkh_scripthash = get_p2pkh_scripthash_from_pubkey(pubkey)
            p2pkh_resp = rpc('blockchain.scripthash.get_balance', p2pkh_scripthash)
            if 'result' in p2pkh_resp:
                if 'confirmed' in p2pkh_resp['result']:
                    p2pkh_confirmed_balance = p2pkh_resp['result']['confirmed']
                    p2pkh_unconfirmed_balance = p2pkh_resp['result']['unconfirmed']
        elif address:
            p2pk_scripthash = get_p2pkh_scripthash_from_address(address)
        else:
            return -1
        p2pk_resp = rpc('blockchain.scripthash.get_balance', p2pk_scripthash)
        if 'result' in p2pk_resp:
            if not isinstance(p2pk_resp['result'], int):
                p2pk_confirmed_balance = p2pk_resp['result']['confirmed']
                p2pk_unconfirmed_balance = p2pk_resp['result']['unconfirmed']

        total_confirmed = p2pk_confirmed_balance + p2pkh_confirmed_balance
        total_unconfirmed = p2pk_unconfirmed_balance + p2pkh_unconfirmed_balance

        total = total_confirmed + total_unconfirmed
        return total/100000000

    def get_p2pkh_scripthash_from_address(address):
        # remove address prefix
        addr_stripped = binascii.hexlify(b58decode_check(address)[1:])
        # Add OP_DUP OP_HASH160 BTYES_PUSHED <ADDRESS> OP_EQUALVERIFY OP_CHECKSIG
        raw_sig_script = b"".join((b"76a914", addr_stripped, b"88ac"))
        script_hash = hashlib.sha256(codecs.decode(
            raw_sig_script, 'hex')).digest()[::-1].hex()
        return script_hash

    def get_p2pk_scripthash_from_pubkey(pubkey):
        scriptpubkey = '21' + pubkey + 'ac'
        script_hash = get_scripthash(scriptpubkey)
        return script_hash

    def get_p2pkh_scripthash_from_pubkey(pubkey):
        publickey = codecs.decode(pubkey, 'hex')
        s = hashlib.new('sha256', publickey).digest()
        r = hashlib.new('ripemd160', s).digest()
        scriptpubkey = "76a914"+codecs.encode(r, 'hex').decode("utf-8")+"88ac"
        script_hash = get_scripthash(scriptpubkey)
        return script_hash

    def get_scripthash(scriptpubkey):
        scripthex = codecs.decode(scriptpubkey, 'hex')
        s = hashlib.new('sha256', scripthex).digest()
        sha256_scripthash = codecs.encode(s, 'hex').decode("utf-8")
        script_hash = self.lil_endian(sha256_scripthash)
        return script_hash



