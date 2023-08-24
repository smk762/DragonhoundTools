#!/usr/bin/env python3
import os
import sys
import json
import requests
import asyncio
from websockets.sync.client import connect

from logger import logger
from os.path import expanduser, dirname, realpath


SCRIPT_PATH = dirname(realpath(__file__))

MM2_JSON_PATH = f"{SCRIPT_PATH}/MM2.json"

class KomoDeFi_API():
    def __init__(self, config: str=MM2_JSON_PATH, protocol: str = "http"):
        ip = '127.0.0.1'
        port = 7783
        netid = 7777
        self.protocol = protocol
        if os.path.isfile(MM2_JSON_PATH):
            with open(MM2_JSON_PATH, "r") as f:
                conf = json.load(f)
            self.userpass = conf["rpc_password"]
            if "rpc_ip" in conf:
                ip = conf["rpc_ip"]
            if "rpcport" in conf:
                port = conf["rpcport"]
            if "netid" in conf:
                self.netid = conf["netid"]
            else: self.netid = 7777
            self.mm2_ip = f"{self.protocol}://{ip}:{port}"
        else:
            logger.error(f"Komodefi SDK config not found at {MM2_JSON_PATH}!")
            raise SystemExit(1)
        version = self.version
        if version == "Error":
            logger.warning(f"Komodefi SDK is not running at {self.mm2_ip}!")
            raise SystemExit(1)
        # logger.debug("-"*80)
        # logger.info(f"Komodefi SDK version {self.version} is running at {self.mm2_ip} on netID {self.netid}!")


    def rpc(self, method, params=None, v2=False, wss=False):
        if not params:
            params = {}
        body = {
            "userpass": self.userpass,
            "method": method
        }
        if v2:
            body.update({
                "mmrpc": "2.0",
                "params": params
            })
        elif params:
            body.update(params)
        if wss:
            with connect(self.mm2_ip) as ws:
                ws.send(json.dumps(body))
                data = ws.recv()
                logger.info(f"Received: {data}")
                return data
        else:
            r = requests.post(self.mm2_ip, json.dumps(body))
        return r
    
    def get_activation_params(self, coin: str, network: str):
        url = "http://116.203.120.91:8762/api/atomicdex/activation_commands/"
        data = requests.get(url).json()["commands"]
        if coin in data:
            return data[coin]
        else:
            return None
        
    @property
    def version(self):
        try:
            return self.rpc("version").json()["result"]
        except ConnectionRefusedError:
            return "Error"


if __name__ == '__main__':
    api = KomoDeFi_API()
