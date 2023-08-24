#!/usr/bin/env python3
import sys
import json
import time
import shutil
from datetime import timedelta
sys.path.append('../../../komodefi')
from kdf_sdk import KomoDeFi_API
from logger import logger
 
# setting path

DB_FOLDER = "DB/b44ed5e144661678428125445141e5131a27dab8"

with open("methods.json", "r") as f:
    methods = json.load(f)

def test_activation(
    coin: str,
    sync_params: dict = None,
    scan_interval: int = 200,
    scan_chunksize: int = 100
) -> dict:
    api = KomoDeFi_API()
    method = "task::enable_z_coin::init"
    params = methods[method]
    activation = api.get_activation_params(coin)
    if activation:
        params["ticker"] = coin
        rpc_data = activation["activation_params"]["mode"]["rpc_data"]
        params["activation_params"]["mode"]["rpc_data"] = rpc_data
        params["activation_params"]["sync_params"] = sync_params
        params["activation_params"]["scan_interval_ms"] = scan_interval
        params["activation_params"]["scan_blocks_per_iteration"] = scan_chunksize
    return api.rpc(method, params, True).json()


def get_sync_params(weeks_ago: int = 1):
    return {
        "earliest": "earliest",
        "date": int(time.time()) - 1440 * 7 * weeks_ago,
        "height": 2 ^ weeks_ago,
    }


def get_activation_status(task_id: int):
    api = KomoDeFi_API()
    method = "task::enable_z_coin::status"
    params = methods[method]
    params["task_id"] = task_id
    return api.rpc(method, params, True).json()


def activation_time(coin, sync, scan_interval, scan_chunksize):
    start = int(time.time())
    r = test_activation(coin, sync, scan_interval, scan_chunksize)
    task_id = r["result"]["task_id"]
    status = None
    while True:
        status = get_activation_status(task_id)
        logger.debug(f"Activation status: {status}...")
        if status["result"]["status"] in ["Ok", "Error"]:
            end = int(time.time())
            outcome = status["result"]["status"]
            disable(coin)
            break
        time.sleep(20)
        
    logger.debug(f"Deleting {DB_FOLDER}...")
    shutil.rmtree(DB_FOLDER)
    return {
        "coin": coin,
        "time": end - start,
        "task_id": task_id,
        "interval_ms": scan_interval,
        "chunksize": scan_chunksize,
        "sync": sync,
        "outcome": outcome
    }
    

def disable(coin):
    api = KomoDeFi_API()
    params = {"coin": coin}
    return api.rpc("disable_coin", params).json()


if __name__ == '__main__':
    results = []
    coin = "ZOMBIE"
    scan_interval = 200
    scan_chunksize = 100
    for i in range(4, 16, 3):
        sync = get_sync_params(i)
        for j in range(3):
            for k in range(3):
                r = activation_time(coin, sync, scan_interval * j, scan_chunksize * k)
                results.append(r)
    
    with open("activation_results.json", "w") as f:
        json.dump(results, f, indent=4)
