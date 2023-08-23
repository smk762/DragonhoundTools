#!/usr/bin/env python3
import os
import json
import requests
from logger import logger

MM2_JSON_PATH = "MM2.json"

class KomoDeFi_API():
    def __init__(self, config=MM2_JSON_PATH):
        self.mm2_ip = f'http://127.0.0.1:7783'
        self.netid = 7777
        if os.path.isfile(MM2_JSON_PATH):
            with open(MM2_JSON_PATH, "r") as f:
                conf = json.load(f)
            self.userpass = conf["rpc_password"]
            if "rpc_ip" in conf:
                self.mm2_ip.replace("127.0.0.1", conf["rpc_ip"])
            if "rpc_port" in conf:
                self.mm2_ip.replace("7783", conf["rpc_port"])
            if "netid" in conf:
                self.netid = conf["netid"]
        else:
            logger.error(f"MM2 config not found at {MM2_JSON_PATH}!")
            raise SystemExit(1)
        version = self.version()
        if version == "Error":
            logger.warning(f"MM2 is not running at {self.mm2_ip}!")
            raise SystemExit(1)
        logger.info(f"MM2 is running [{version}] at [{self.mm2_ip}] on netID [{self.netid}]!")
           
    def rpc(self, method, params=None):
        if not params:
            params = {}
        params.update({
            "method": method,
            "userpass": self.userpass
        })
        r = requests.post(self.mm2_ip, json.dumps(params))
        return r

    def version(self):
        try:
            return self.rpc("version").json()["result"]
        except ConnectionRefusedError:
            return "Error"


if __name__ == '__main__':
    api = KomoDeFi_API()
    print(api.version())
    