#!/usr/bin/env python3
import os
import sys
import json
import time
import shutil
from datetime import timedelta
sys.path.append('../../../komodefi')
from kdf_sdk import KomoDeFi_API
from logger import logger
 
# setting path

DB_FOLDER = "/home/smk762/GITHUB/SMK/DragonhoundTools/komodefi/DB/b44ed5e144661678428125445141e5131a27dab8"

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
    activation = api.get_activation_params(coin, "ZHTLC")
    params["ticker"] = coin
    params["activation_params"]["sync_params"] = sync_params
    params["activation_params"]["scan_interval_ms"] = scan_interval
    params["activation_params"]["scan_blocks_per_iteration"] = scan_chunksize
    logger.info(f"Activation params for {coin}: {params}")
    return api.rpc(method, params, True).json()


def get_sync_params(weeks_ago: int = 1):
    return {
        "bad_key": "bad_key",
        "earliest": "earliest",
        "date": {"date": int(time.time()) - 1440 * 7 * weeks_ago},
        "height": {"date": 2 ^ weeks_ago},
    }


def get_activation_status(task_id: int):
    api = KomoDeFi_API()
    method = "task::enable_z_coin::status"
    params = methods[method]
    if "task_id" in params:
        params["task_id"] = task_id
        return api.rpc(method, params, True).json()
    else:
        logger.error(f"Task ID {task_id} not found in {method} params!")
        raise SystemExit(1)


def activation_time(coin, sync, scan_interval, scan_chunksize):
    disable(coin)
    start = int(time.time())
    r = test_activation(coin, sync, scan_interval, scan_chunksize)
    if "result" not in r:
        return r
    task_id = r["result"]["task_id"]
    status = None
    while True:
        status = get_activation_status(task_id)
        logger.debug(f"Activation status: {status}...")
        if status["result"]["status"] in ["Ok", "Error"]:
            end = int(time.time())
            outcome = status["result"]["status"]
            break
        time.sleep(20)
    delete_cache()
    return {
        "coin": coin,
        "time": end - start,
        "task_id": task_id,
        "interval_ms": scan_interval,
        "chunksize": scan_chunksize,
        "sync": sync,
        "outcome": outcome
    }

def delete_cache():        
    logger.debug(f"Deleting {coin} cache data from {DB_FOLDER}...")
    try:
        os.remove(f"{DB_FOLDER}/{coin}_cache.db")
    except FileNotFoundError:
        pass
    try:
        os.remove(f"{DB_FOLDER}/{coin}_wallet.db")
    except FileNotFoundError:
        pass

def disable(coin):
    api = KomoDeFi_API()
    params = {"coin": coin}
    return api.rpc("disable_coin", params).json()


if __name__ == '__main__':
    results = []
    coin = "ZOMBIE"
    scan_interval = 205
    scan_chunksize = 140
    for i in range(-1, 16, 5):
        sync = get_sync_params(i)
        for x in sync:
            sync_params = sync[x]
            for j in range(-1,16, 5):
                for k in range(-1,16, 5):
                    logger.debug("-"*80)
                    logger.info(f"Testing activation with sync_params: {sync_params}, scan_interval: {scan_interval * j}, scan_chunksize: {scan_chunksize * k}...")
                    r = activation_time(coin, sync_params, scan_interval * j, scan_chunksize * k)
                    results.append(r)
                    if "outcome" in r:
                        if r["outcome"]["error"]:
                            logger.warning(r)
                        else:
                            logger.info(r)
                    else:
                        logger.error(r)
    
    with open("activation_results.json", "w") as f:
        json.dump(results, f, indent=4)
