#!/usr/bin/env python3
import os
import time
import base58
import hashlib
import bitcoin
import binascii
from bitcoin.core import x
from bitcoin.core import CoreMainParams
from bitcoin.wallet import P2PKHBitcoinAddress
from logger import logger

BASE58_PARAMS = {
    "LTC": {'pubtype': 48, 'wiftype': 5, 'p2shtype': 176},
    "AYA": {"pubtype": 23, "wiftype": 176, "p2shtype": 5},
    "EMC2": {"pubtype": 33, "wiftype": 176, "p2shtype": 5},
    "KMD": {"pubtype": 60, "wiftype": 188, "p2shtype": 85},
    "MIL": {"pubtype": 50, "wiftype": 239, "p2shtype": 196}
}

def get_CoinParams(coin):
    params = BASE58_PARAMS[coin]
    class CoinParams(CoreMainParams):
        MESSAGE_START = b'\x24\xe9\x27\x64'
        DEFAULT_PORT = 7770
        BASE58_PREFIXES = {
            'PUBKEY_ADDR': params["pubtype"],
            'SCRIPT_ADDR': params["p2shtype"],
            'SECRET_KEY': params["wiftype"]
        }
    return CoinParams


coin_params = {}
for coin in BASE58_PARAMS:
    coin_params[coin] = get_CoinParams(coin)


def lil_endian(hex_str):
    return ''.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)][::-1])


def get_addr_from_pubkey(pubkey: str, coin: str="KMD") -> str:
    if coin not in coin_params:
        coin = "KMD"
    bitcoin.params = coin_params[coin]
    try:
        return str(P2PKHBitcoinAddress.from_pubkey(x(pubkey)))
    except Exception as e:
        os.system('clear')
        print(f"\n\n")
        logger.error(f"Error! {e}")
        print(f"\n\n")
        time.sleep(1)
        return ""

def convert_address(address: str, coin: str="KMD"):
    decoded_bytes = bitcoin.base58.decode(address)
    addr_format = decoded_bytes[0]    # PUBKEY_ADDR
    addr = decoded_bytes[1:-4]        # RIPEMD-160 hash
    checksum = decoded_bytes[-4:]
    calculated_checksum = bitcoin.core.Hash(decoded_bytes[:-4])[:4]

    if checksum != calculated_checksum:
        print(f"Checksum {coin} mismatch: expected {checksum}, got {calculated_checksum}")

    new_format = coin_params[coin]['pubtype']
    if new_format < 16:
        new_addr_format = f"0{hex(new_format)[2:]}"
    else:
        new_addr_format = hex(new_format)[2:]

    new_ripemedhash = new_addr_format.encode(
        'ascii') + binascii.hexlify(addr)
    # first 4 bytes, sha256 new_ripemedhash twice
    checksum = doubleSha256(new_ripemedhash)[:4]
    ripemedhash_full = new_ripemedhash + binascii.hexlify(checksum)
    new_address = bitcoin.base58.encode(
        binascii.unhexlify(ripemedhash_full))

def sha256(data):
    d = hashlib.new("sha256")
    d.update(data)
    return d.digest()


def ripemd160(x):
    d = hashlib.new("ripemd160")
    d.update(x)
    return d.digest()


def doubleSha256(hex_str):
    hexbin = binascii.unhexlify(hex_str)
    binhash = hashlib.sha256(hexbin).digest()
    hash2 = hashlib.sha256(binhash).digest()
    return hash2


def get_hex(val, byte_length=2, endian='big'):
    val = hex(int(val))[2:]
    pad_len = byte_length - len(val)
    val = pad_len*"0"+val
    if endian == 'little':
        val = lil_endian(val)
    return val


def get_hash160(pubkey):
    bin_pk = binascii.unhexlify(pubkey)
    sha_pk = sha256(bin_pk)
    ripe_pk = ripemd160(sha_pk)
    return binascii.hexlify(ripe_pk)


def address_to_p2pkh(address):
    decode_58 = bitcoin.base58.decode(address)
    decode_58 = decode_58[1:-4]
    pubKeyHash = "76a914"+binascii.hexlify(decode_58).decode('ascii')+"88ac"
    return pubKeyHash


def pubkey_to_p2pkh(pubkey):
    hash160 = get_hash160(pubkey)
    p2pkh = "76a914"+hash160.decode('ascii')+"88ac"
    return p2pkh


def pubkey_to_p2pk(pubkey):
    hash160 = get_hash160(pubkey)
    p2pk = "21"+pubkey+"ac"
    return p2pk


OP_CODES = {
    "OP_RETURN": "6a",
    "OP_PUSHDATA1": "4c",
    "OP_PUSHDATA2": "4d",
    "OP_CHECKSIG": "ac", 
    "OP_FALSE": "00",
    "OP_IF": "63",
    "OP_NOTIF": "64",
    "OP_ELSE": "67",
    "OP_ENDIF": "68",
    "OP_VERIFY": "69",
    "OP_DUP": "76"
}


