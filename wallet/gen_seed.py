#!/bin/python3
import secrets
import binascii
import mnemonic # pip3 install mnemonic==0.20
import bip32utils # pip3 install bip32utils==0.3.post4
from wordlist import english_wordlist 

secretsGenerator = secrets.SystemRandom()

 
 
def gen_seed(length=24):
    """Generate a random seed of length words."""
    words = ' '.join(secrets.choice(english_wordlist) for _ in range(length - 1))
    checksum = get_checksum_word(words)
    return f"{words} {checksum}"

def get_checksum_word(seed):
    valid = []
    m = mnemonic.Mnemonic('english')
    for word in english_wordlist:
        tested = f"{seed} {word}"
        if m.check(tested):
            valid.append(word)
    return secrets.choice(valid)

def get_seed(seed_phrase):
    m = mnemonic.Mnemonic('english')
    return m.to_seed(seed_phrase)


if __name__ == '__main__':
    length = input("> Do you want a 12 or 24 word seed? ")
    while length not in ['12', '24']:
        print(f"Invalid input: {length}. Must be 12 or 24!\n")
        length = input("> Do you want a 12 or 24 word seed? ")
    seed_phrase = gen_seed(int(length))
    print(f"\nSeed Phrase:\n\n {seed_phrase}\n\n")