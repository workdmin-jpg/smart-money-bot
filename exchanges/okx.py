# exchanges/okx.py
import json
import urllib.request

OKX_URL = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"


def get_okx_spot_usdt():
    markets = []

    try:
        req = urllib.request.Request(
            OKX_URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        for item in data["data"]:
            symbol = item["instId"]

            if not symbol.endswith("-USDT"):
                continue

            markets.append({
                "exchange": "OKX",
                "symbol": symbol.replace("-", ""),
                "price": float(item["last"]),
                "volume": float(item["volCcy24h"])
            })

    except Exception as e:
        print("⚠️ OKX error:", e)

    return markets