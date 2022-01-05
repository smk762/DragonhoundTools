#!/usr/bin/env python3
import os
import sys
import time
import hashlib
import os.path
import pathlib
from pprint import pprint
import requests
from virustotal_python import Virustotal
from dotenv import load_dotenv
from lib_color import *

load_dotenv()
SCRIPT_PATH = sys.path[0]
VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY')

HEADERS = {
    "Accept": "application/json",
    "x-apikey": VIRUSTOTAL_API_KEY
}

vtotal = Virustotal(API_KEY=VIRUSTOTAL_API_KEY, API_VERSION="v3", TIMEOUT=600)


def send_file_to_vt(file_with_path, large_file_url=None):
    files = {"file": (os.path.basename(file_with_path), open(os.path.abspath(file_with_path), "rb"))}

    if large_file_url:
        r = vtotal.request(large_file_url, files=files, method="POST", large_file=True)
    else:
        r = vtotal.request("files", files=files, method="POST")
    return r.json()


def get_large_upload_url():
    url = "https://www.virustotal.com/api/v3/files/upload_url"

    r = requests.request("GET", url, headers=HEADERS)
    upload_url = r.json()["data"]
    return upload_url


def get_sha256(analysis_identifier):
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_identifier}/relationships/item"
    r = requests.request("GET", url, headers=HEADERS)

    i = 0
    while not r.json()["data"]:
        i += 1
        info_print(f"Data result is empty, trying again ({i}/5)")
        time.sleep(20)
        r = requests.request("GET", url, headers=HEADERS)

        if i == 5:
            error_print("==================================")
            error_print("Unable to get id after 5 tries...")
            error_print(r)
            error_print(r.json())
            error_print("==================================")
            return None

    if "id" in r.json()["data"]:
        return r.json()['data']['id']

    error_print("==================================")
    error_print("No ID in analysis item data")
    error_print(r)
    error_print(r.json())
    error_print("==================================")
    return None
    

def calc_sha256(fn):
    with open(fn,"rb") as f:
        sha256_hash = hashlib.sha256()

        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def has_it_been_a_minute(ts):
    if int(time.time()) - int(ts) > 60:
        return True
    return False


def does_report_exist(sha256_sum):
    url = f"https://www.virustotal.com/api/v3/files/{sha256_sum}"

    r = requests.request("GET", url, headers=HEADERS)

    if 'error' in r.json():
        return False
    return True


def get_vt_hash(file):

    try:
        sha256_sum = calc_sha256(file)

        if not does_report_exist(sha256_sum):
            info_print(f"Submitting {file} to VirusTotal...")
            ts = time.time()
            url = get_large_upload_url()

            while not has_it_been_a_minute(ts):
                time.sleep(15)
            ts = time.time()

            #print(f"URL: {url}")
            resp = send_file_to_vt(f'{file}', url)

            while not has_it_been_a_minute(ts):
                time.sleep(15)
            ts = time.time()

            #print(resp)
            analysis_identifier = resp["data"]["id"]
            sha256_sum = get_sha256(analysis_identifier)
            while not has_it_been_a_minute(ts):
                time.sleep(15)
            ts = time.time()
        else:
            status_print(f"Report for {file} already available!")

        success_print(f"https://www.virustotal.com/gui/file/{sha256_sum}")
        return sha256_sum

    except Exception as e:
        error_print(f"Error: {e}")
        return "Failed"
