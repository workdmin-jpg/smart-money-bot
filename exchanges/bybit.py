# exchanges/bybit.py
import json
import urllib.request

BYBIT_URL = "https://api.bybit.com/v5/market/tickers?category=spot"


def get_bybit_spot_usdt():
    with urllib.request.urlopen(BYBIT_URL, timeout=10) as response:
        data = json.loads(response.read().decode())

    markets = []

    for item in data["result"]["list"]:
        symbol = item["symbol"]

        if not symbol.endswith("USDT"):
            continue

        markets.append({
            "exchange": "BYBIT",
            "symbol": symbol,
            "price": float(item["lastPrice"]),
            "volume": float(item["turnover24h"])
        })

    return markets