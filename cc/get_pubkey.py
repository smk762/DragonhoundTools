#!/usr/bin/env python3
import os
import sys
import json
from os.path import expanduser
home = expanduser("~")
try:
    with open(home+"/DragonhoundTools/config/config.json") as j:
        config_json = json.load(j)
except Exception as e:
    print("config.json has error or does not exist!")
    print(e)
    print("Create one using the template:")
    print("cp "+home+"/DragonhoundTools/config/config_example.json "+home+"/DragonhoundTools/config/config.json")
    print("nano "+home+"/DragonhoundTools/config/config.json")
    sys.exit(0)

print(config_json['pubkey'])
