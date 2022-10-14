#!/usr/bin/env python3
import os
import json

# simple key sort
for i in os.listdir("."):
    if i.endswith(".json"):
        with open(i, "r") as f:
            data = json.load(f)

        with open(i, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)
