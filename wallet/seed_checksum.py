#!/bin/python3

import mnemonic
from wordlist import english_wordlist 
 
m = mnemonic.Mnemonic('english')
for word in english:
    tested = f"{seed} {word}"
    if m.check(tested):
        print(tested)
