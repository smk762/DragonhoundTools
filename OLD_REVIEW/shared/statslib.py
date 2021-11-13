#!/usr/bin/env python3
import sys
import os

from kmdlib import *

def stats2oracle(rpc, oracletxid, message):
    rawhex = codecs.encode(message).hex()
    bytelen = int(len(rawhex) / int(2))
    hexlen = format(bytelen, 'x')
    if bytelen < 16:
        bigend = "000" + str(hexlen)
    elif bytelen < 256:
        bigend = "00" + str(hexlen)
    elif bytelen < 4096:
        bigend = "0" + str(hexlen)
    elif bytelen < 65536:
        bigend = str(hexlen)
    else:
        print("ORACLE WRITE ERROR: Message too large, must be less than 65536 characters")
    lilend = bigend[2] + bigend[3] + bigend[0] + bigend[1]
    fullhex = lilend + rawhex
    oraclesdata_result = rpc.oraclesdata(oracletxid, fullhex)
    result = oraclesdata_result['result']
    if result == 'error':
        print('ORACLE WRITE ERROR:' + oraclesdata_result['error'] + ', try using oraclesregister if you have not already, and check the oracle is funded')
    else:
        rawtx = oraclesdata_result['hex']
        sendrawtransaction_result = rpc.sendrawtransaction(rawtx)
        print(colorize("Stats written to oracle at http://oracle.earth/oracle_samples/?chain=ORACLEARTH&oracletxid="+stats_oracletxid+"&batonutxo=&num=20.", 'blue'))
    return result
