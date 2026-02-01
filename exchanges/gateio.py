# exchanges/gateio.py
import json
import urllib.request

GATE_URL = "https://api.gateio.ws/api/v4/spot/tickers"


def get_gateio_spot_usdt():
    markets = []

    try:
        with urllib.request.urlopen(GATE_URL, timeout=10) as response:
            data = json.loads(response.read().decode())

        for item in data:
            symbol = item.get("currency_pair", "")

            if not symbol.endswith("_USDT"):
                continue

            last = item.get("last")
            volume = item.get("quote_volume")

            if not last or not volume:
                continue

            price = float(last)
            volume = float(volume)

            if price <= 0 or volume <= 0:
                continue

            markets.append({
                "exchange": "GATEIO",
                "symbol": symbol.replace("_", ""),
                "price": price,
                "volume": volume
            })

    except Exception as e:
        print("⚠️ Gate.io error:", e)

    return markets