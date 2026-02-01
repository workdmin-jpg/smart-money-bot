# context/cmc.py
# ===============================
# CoinMarketCap Context Score
# ===============================

import json
import urllib.request
from datetime import datetime, timedelta

from settings import CMC_API_KEY


CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"


def get_coinmarketcap_score(symbol, days=3):
    """
    Returns score 0–40 based on:
    - market cap rank
    - volume change
    - price change (last 24h)
    """

    if not CMC_API_KEY:
        return 0

    base_symbol = symbol.replace("USDT", "")

    params = f"?symbol={base_symbol}&convert=USD"
    req = urllib.request.Request(
        CMC_URL + params,
        headers={
            "X-CMC_PRO_API_KEY": CMC_API_KEY,
            "Accepts": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())

        coin = data["data"][base_symbol]["quote"]["USD"]

        score = 0

        # Volume activity
        if coin["volume_change_24h"] > 10:
            score += 15
        elif coin["volume_change_24h"] > 0:
            score += 8

        # Price momentum
        if coin["percent_change_24h"] > 5:
            score += 15
        elif coin["percent_change_24h"] > 0:
            score += 8

        # Market cap strength
        if coin["market_cap"] > 1_000_000_000:
            score += 10

        return min(score, 40)

    except Exception as e:
        print(f"CMC ERROR {symbol}: {e}")
        return 0