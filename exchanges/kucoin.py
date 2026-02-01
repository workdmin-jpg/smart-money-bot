# exchanges/kucoin.py
import json
import urllib.request

KUCOIN_URL = "https://api.kucoin.com/api/v1/market/allTickers"


def get_kucoin_spot_usdt():
    with urllib.request.urlopen(KUCOIN_URL, timeout=10) as response:
        data = json.loads(response.read().decode())

    markets = []

    for item in data["data"]["ticker"]:
        symbol = item["symbol"]

        if not symbol.endswith("-USDT"):
            continue

        markets.append({
            "exchange": "KUCOIN",
            "symbol": symbol.replace("-", ""),
            "price": float(item["last"]),
            "volume": float(item["volValue"])
        })

    return markets