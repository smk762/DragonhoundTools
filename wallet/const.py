#!/usr/bin/env python3
import os
import sys
from os.path import expanduser, dirname, realpath

INSIGHT_EXPLORERS = {
    'CCL': 'https://ccl.explorer.dexstats.info/',
    'CHIPS': 'https://chips.explorer.dexstats.info/',
    'CLC': 'https://clc.explorer.dexstats.info/',
    'DOC': 'https://doc.dragonhound.info/',
    'GLEEC': 'https://gleec.explorer.dexstats.info/',
    'ILN': 'https://iln.explorer.dexstats.info/',
    'KMD': 'https://kmd.explorer.dexstats.info/',
    'KMD_3P': 'https://kmd.explorer.dexstats.info/',
    'KOIN': 'https://koin.explorer.dexstats.info/',
    'MARTY': 'https://marty.dragonhound.info/',
    'MCL': 'https://mcl.explorer.dexstats.info/',
    'NINJA': 'https://ninja.explorer.dexstats.info/',
    'PIRATE': 'https://explorer.pirate.black/',
    'SUPERNET': 'https://supernet.explorer.dexstats.info/',
    'THC': 'https://thc.explorer.dexstats.info/',
    'TOKEL': 'https://tokel.explorer.dexstats.info/',
    'VRSC': 'https://vrsc.explorer.dexstats.info/'
}

CRYPTOID_API_KEY = os.getenv('CRYPTOID_API_KEY')
CRYPTOID_EXPLORERS = {
    'EMC2': 'https://chainz.cryptoid.info/emc2/',
    'MIL': 'https://chainz.cryptoid.info/mil/'
}
BLOCKCYPHER_EXPLORERS = {
    'LTC': 'https://api.blockcypher.com/v1/ltc/main'
}
NO_EXPLORER = {
    'AYA': ''
}

HOME = expanduser('~')
SCRIPT_PATH = dirname(realpath(sys.argv[0]))
COINS_CONFIG_URL = "https://raw.githubusercontent.com/KomodoPlatform/coins/master/utils/coins_config.json"
COINS_CONFIG_PATH = f"{SCRIPT_PATH}/coins_config.json"

COMMIT_HASHES_URL = "https://raw.githubusercontent.com/KomodoPlatform/dPoW/master/README.md"
COMMIT_HASHES_PATH = f"{SCRIPT_PATH}/commit_hashes.json"

SEEDNODE_VERSIONS_URL = "https://raw.githubusercontent.com/KomodoPlatform/dPoW/seednode-update/doc/seed_version_epochs.json"
SEEDNODE_VERSIONS_PATH = f"{SCRIPT_PATH}/seed_versions.json"

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

