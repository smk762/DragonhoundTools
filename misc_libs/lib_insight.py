import requests

# Grabs data from Insight explorer APIs
# e.g. https://kmd.explorer.dexstats.info/insight-api-komodo


def get_utxos(coin, address):
    try:
        subdomain = f"https://{coin.lower()}.explorer.dexstats.info"
        endpoint = f"insight-api-komodo/addr/{address}/utxo"
        return requests.get(f"{subdomain}/{endpoint}").json()
    except Exception as e:
        return f"{e}"


def get_sync(coin):
    try:
        subdomain = f"https://{coin.lower()}.explorer.dexstats.info"
        endpoint = "/insight-api-komodo/sync"
        return requests.get(f"{subdomain}/{endpoint}").json()
    except Exception as e:
        return f"{e}"


def get_block_info(coin, block_height):
    try:
        subdomain = f"https://{coin.lower()}.explorer.dexstats.info"
        endpoint = f"/insight-api-komodo/block-index/{block_height}"
        return requests.get(f"{subdomain}/{endpoint}").json()
    except Exception as e:
        return f"{e}"


def get_balance(coin, addr):
    try:
        subdomain = f"https://{coin.lower()}.explorer.dexstats.info"
        endpoint = f"/insight-api-komodo/addr/{addr}"
        return requests.get(f"{subdomain}/{endpoint}").json()
    except Exception as e:
        return f"{e}"
