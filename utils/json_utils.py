#!/usr/bin/env python3
import os
import csv
import json

# simple key sort
def sort_json_files():
    for i in os.listdir("."):
        if i.endswith(".json"):
            with open(i, "r") as f:
                data = json.load(f)
            with open(i, "w") as f:
                json.dump(data, f, indent=4, sort_keys=True)



def convert_csv(file, has_headers=False):
    for i in os.listdir("."):
        if i.endswith(".csv"):
            with open(i, "r") as f:
                csv_reader = csv.DictReader(f)
                line_count = 0
                data = []
                for row in csv_reader:
                    data.append(row)
                    line_count += 1
                print(f'Processed {line_count} lines.')
            with open(i, "w") as f:
                json.dump(data, f, indent=4, sort_keys=True)


