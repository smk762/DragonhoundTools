## Wallet Tools

### `./reindex.sh [ac_name]`
Stops chain (passed as param), then restarts it with reindex flag. Requires `pubkey.txt` in komodo/src

### `./restart.sh [ac_name]`
Stops chain (passed as param), then restarts it. Requires `pubkey.txt` in komodo/src

### `./add_whiteRadd.sh [R-address]`
Adds R-address (passed as param) to all assetchain conf files.

### `./clean_dust.sh [ac_name]`
Combines dust utxos to recover from a dwy shotgun attack (you wont need this if you use whitlist addresses).

### `./importprivkey.py [wif]`
Imports a private key (passed as param) to all assetchain wallets.

