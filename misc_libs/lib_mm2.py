#!/usr/bin/env python3
import requests

def mm2_proxy(params):
    params.update({"userpass": MM2_USERPASS})
    try:
        r = requests.post(MM2_IP, json.dumps(params))
        resp = r.json()
    except requests.exceptions.RequestException as e:
        start_mm2()
        r = requests.post(MM2_IP, json.dumps(params))
        resp = r.json()
        if "error" in resp:
            if resp["error"].find("Userpass is invalid"):
                error_print("MM2 is rejecting your rpc_password. Please check you are not running mm2 or AtomicDEX-Desktop app, and your rpc_password conforms to constraints in https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-setup/configure-mm2-json.html#mm2-json")
                sys.exit()
    return resp


def get_version():
    params = {"method":"version"}
    resp = mm2_proxy(params)
    return resp


def stop_mm2():
    params = {"method":"stop"}
    resp = mm2_proxy(params)
    return resp
  


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/my_balance.html
def get_balance(coin):
    return mm2_proxy({"method":"my_balance","coin":coin})


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/disable_coin.html
def disable_coin(coin):
    return mm2_proxy({"method":"disable_coin","coin":coin})


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-20/withdraw.html
def withdraw(coin, amount, address):
    if amount == "MAX":
        return mm2_proxy({"mmrpc":"2.0","method":"withdraw","params":{"coin":coin,"to":address,"max":True},"id":0})
    else:
        return mm2_proxy({"mmrpc":"2.0","method":"withdraw","params":{"coin":coin,"to":address,"amount":amount},"id":0})


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/send_raw_transaction.html
def send_raw_tx(coin, tx_hex):
    return mm2_proxy({"method":"send_raw_transaction","coin":coin,"tx_hex":tx_hex})


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/validateaddress.html
def validate_address(coin, address):
    return mm2_proxy({"method":"validateaddress","coin":coin,"address":address})


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/validateaddress.html
def is_address_valid(coin, address):
    return validate_address(coin, address)["result"]["is_valid"]

# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/my_orders.html
def get_orders():
    return mm2_proxy({"method":"my_orders"})


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/my_recent_swaps.html
def get_recent_swaps(limit=1000):
    return mm2_proxy({"method":"my_recent_swaps","limit":limit})


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/active_swaps.html
def get_active_swaps():
    return mm2_proxy({"method":"active_swaps", "include_status": True})


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/cancel_all_orders.html
def cancel_all_orders():
    return mm2_proxy({"method":"cancel_all_orders","cancel_by":{"type":"All"}})


# https://developers.komodoplatform.com/basic-docs/atomicdex-api-legacy/validateaddress.html
def validate_withdraw_amount(amount):
    if amount in ["MAX", "max"]:
        return "MAX"
    else:
        try:
            return float(amount)
        except:
            return False
