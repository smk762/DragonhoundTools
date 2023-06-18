#!/bin/python3

import mnemonic
from wordlist import english_wordlist 
 
m = mnemonic.Mnemonic('english')
seed_without_checksum_word = input("Enter the first 11 or 23 words: ")
for word in english:
    tested = f"{seed_without_checksum_word} {word}"
    if m.check(tested):
        print(tested)
