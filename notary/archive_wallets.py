#!/usr/bin/env python3
import os
import sys
import socket
from zipfile import ZipFile

def migrate_wallets(season, region):
    home = os.path.expanduser("~")
    wallet_folders = [
        ".aryacoin", ".chips", ".einsteinium",
        ".komodo", ".komodo_3p", ".mil"
    ]

    output_path = f"{home}/wallets"
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    wallet_folders_main = []
    wallet_folders_3p = []

    if os.path.exists(".komodo"):
        wallet_folders_main = [f".komodo/{i}" for i in os.listdir(f"{home}/.komodo") if i[0] == i[0].upper() and os.path.isdir(i) and len(i) > 2]
    if os.path.exists(".komodo_3p"):
        wallet_folders_3p = [f".komodo_3p/{i}" for i in os.listdir(f"{home}/.komodo_3p") if i[0] == i[0].upper() and os.path.isdir(i) and len(i) > 2]

    folders = list(set(wallet_folders + wallet_folders_main + wallet_folders_3p))

    zips = []
    for server in ["main", "3p"]:
        for folder in folders:
            print(folder)
            wallets = [x for x in os.listdir(f"{home}/{folder}") if x.endswith('.dat') and x.startswith('wallet')]
            if os.path.exists(folder):
                coin = folder.replace(".", "").split("/")[-1]
                fn = f"{season}_{region}_{server}_{coin}.zip"
                output_zip = f"{output_path}/{fn}"
                with ZipFile(output_zip,'w') as zip:
                    for wallet in wallets:
                        print(f"Archiving {home}/{folder}/{wallet} to {output_zip}")
                        zip.write(f"{home}/{folder}/{wallet}")
                zips.append(output_zip)

    print("Exfiltrate with:")
    for z in zips:
        print(f"rsync {os.getlogin()}@{socket.gethostbyname(socket.gethostname())}:{z} .")

if __name__ == "__main__":
    season = input("Season: ")
    region = input("Region: ")
    migrate_wallets(season, region)
