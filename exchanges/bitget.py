# exchanges/bitget.py
import json
import urllib.request

BITGET_URL = "https://api.bitget.com/api/v2/spot/market/tickers"


def get_bitget_spot_usdt():
    markets = []

    try:
        with urllib.request.urlopen(BITGET_URL, timeout=10) as response:
            data = json.loads(response.read().decode())

        for item in data.get("data", []):
            symbol = item.get("symbol", "")

            if not symbol.endswith("USDT"):
                continue

            last = item.get("last")
            volume = item.get("quoteVolume")

            if not last or not volume:
                continue

            price = float(last)
            volume = float(volume)

            if price <= 0 or volume <= 0:
                continue

            markets.append({
                "exchange": "BITGET",
                "symbol": symbol,
                "price": price,
                "volume": volume
            })

    except Exception as e:
        print("⚠️ Bitget error:", e)

    return markets