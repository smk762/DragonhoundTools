#!/usr/bin/env python3
import csv

# This script takes a CSV file as input and generates a SSH config file
# that can be used to connect to the servers listed in the CSV file.
# The CSV file should have the following format:
# server_name, username, ip_address, ssh_port, ssh_key_file[optional]
# Use the generated config file as `~/.ssh/config`

def add_entry(row, f):
    f.write("Host " + row[0] + "\n")
    f.write("    User " + row[1] + "\n")
    f.write("    HostName " + row[2] + "\n")
    f.write("    Port " + row[3] + "\n")
    if len(row) == 5:
        f.write("    IdentitiesOnly yes\n")
        f.write("    IdentityFile " + row[4] + "\n\n")
    f.write("\n")


def convert_csv_to_ssh_config(csv_file, ssh_config_file="config"):
    rows = []
    with open(ssh_config_file, 'w+') as f:
        # Add the default github.com entry
        f.write("Host github.com\n")
        f.write("    User git\n")
        f.write("    HostName ssh.github.com\n")
        f.write("    Port 443\n")
        f.write("    IdentitiesOnly yes\n")
        f.write("\n")

        with open(csv_file, 'r') as c:
            csvreader = csv.reader(c)
            for row in csvreader:
                add_entry(row, f)
 
if __name__ == "__main__":
    convert_csv_to_ssh_config("servers.csv")
