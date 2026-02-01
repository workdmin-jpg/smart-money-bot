# exchanges/mexc.py
import json
import urllib.request

from exchanges.binance import MEXC_24H

MEXC_24H = "https://api.mexc.com/api/v3/ticker/24hr"


def get_mexc_spot_usdt():
    """
    جلب جميع أزواج USDT من MEXC Spot (Crypto فقط)
    """
    with urllib.request.urlopen(MEXC_24H, timeout=10) as response:
        data = json.loads(response.read().decode())

    markets = []

    for item in data:
        symbol = item.get("symbol", "")

        if not symbol.endswith("USDT"):
            continue

        price = float(item.get("lastPrice", 0))
        volume = float(item.get("quoteVolume", 0))

        # حذف الأزواج الميتة أو بدون سيولة
        if price <= 0 or volume <= 0:
            continue

        markets.append({
            "exchange": "MEXC",
            "symbol": symbol,
            "price": price,
            "volume": volume
        })

    return markets