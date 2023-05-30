#!/usr/bin/env python3
import sys
import requests
import hashlib
import binascii
import base58


def hash160(hexstr):
    preshabin = binascii.unhexlify(hexstr)
    my160 = hashlib.sha256(preshabin).hexdigest()
    return(hashlib.new('ripemd160', binascii.unhexlify(my160)).hexdigest())


def addr_from_ripemd(prefix, ripemd):
    net_byte = prefix + ripemd
    bina = binascii.unhexlify(net_byte)
    sha256a = hashlib.sha256(bina).hexdigest()
    binb = binascii.unhexlify(sha256a)
    sha256b = hashlib.sha256(binb).hexdigest()
    hmmmm = binascii.unhexlify(net_byte + sha256b[:8])
    final = base58.b58encode(hmmmm)
    return(final.decode())


def WIFdecode(WIF):
    b58decode = base58.b58decode(WIF)
    full_privkey = binascii.hexlify(b58decode)
    raw_privkey = full_privkey[2:-8]
    return(raw_privkey.decode("utf-8"))


def WIF_uncompressed(byte, raw_privkey):
    extended_key = byte+raw_privkey
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key[:66])).hexdigest()
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # add checksum to end of extended key
    final_key = extended_key[:66]+second_sha256[:8]
    # Wallet Import Format = base 58 encoded final_key
    WIF = base58.b58encode(binascii.unhexlify(final_key))
    return(WIF.decode("utf-8"))


def WIF_compressed(byte, raw_privkey):
    extended_key = byte+raw_privkey+'01'
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key[:68])).hexdigest()
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # add checksum to end of extended key
    final_key = extended_key[:68]+second_sha256[:8]
    # Wallet Import Format = base 58 encoded final_key
    WIF = base58.b58encode(binascii.unhexlify(final_key))
    return(WIF.decode("utf-8"))


def get_base58_params():
    url = "https://stats.kmd.io/api/info/base_58/"
    return requests.get(url).json()["results"]


def get_wiftype(coin):
    params = get_base58_params()
    if coin not in params:
        print(f"Coin {coin} not found in base 58 params")
        sys.exit(1)
    else:
        return params[coin]["wiftype"]


def int_to_hexstr(x):
    if x == 0: return '00'
    hex_chars = '0123456789ABCDEF'
    hex_string = ''
    while x > 0:
        r = x % 16
        hex_string = hex_chars[r] + hex_string
        x = x // 16
    return hex_string


def wif_convert(coin, wif):
    raw_privkey = WIFdecode(wif)
    wiftype = get_wiftype(coin)
    wiftype_hex = int_to_hexstr(wiftype)
    return WIF_compressed(wiftype_hex, raw_privkey)


if __name__ == '__main__':
    if len(sys.argv[1]) != 3:
        print('Usage: ./helpers.py <coin> <wif>')
        sys.exit(1)
    else:
        coin = sys.argv[1]
        wif = sys.argv[2]
        print(wif_convert(coin, wif))

