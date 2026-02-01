# exchanges/binance.py
import json
import urllib.request

BINANCE_24H = "https://api.binance.com/api/v3/ticker/24hr"
MEXC_24H = {}

def get_binance_spot_usdt():
    """
    جلب جميع أزواج USDT من Binance Spot (Crypto فقط)
    """
    with urllib.request.urlopen(BINANCE_24H, timeout=10) as response:
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
            "exchange": "BINANCE",
            "symbol": symbol,
            "price": price,
            "volume": volume
        })

    return markets