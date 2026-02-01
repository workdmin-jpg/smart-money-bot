import json
import urllib.request
import urllib.parse

# ==============================
# MEXC FUTURES (USDT-M)
# ==============================

BASE_URL = "https://contract.mexc.com/api/v1/contract/kline"


def _fetch_klines(symbol: str, interval: str, limit: int = 200):
    """
    Fetch futures klines from MEXC
    Symbol format example: BTCUSDT -> BTC_USDT
    """

    mexc_symbol = symbol.replace("USDT", "_USDT")

    params = urllib.parse.urlencode({
        "symbol": mexc_symbol,
        "interval": interval,
        "limit": limit
    })

    url = f"{BASE_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            raw = json.loads(response.read().decode())

        if not raw.get("success"):
            return None

        klines = []
        for k in raw["data"]:
            klines.append([
                k["time"],              # timestamp
                float(k["open"]),       # open
                float(k["high"]),       # high
                float(k["low"]),        # low
                float(k["close"]),      # close
                float(k["vol"])         # volume
            ])

        return klines

    except Exception as e:
        print(f"⚠️ MEXC Futures error {symbol}: {e}")
        return None


# ==============================
# Timeframes (Futures)
# ==============================

def get_mexc_futures_klines_5m(symbol, limit=200):
    return _fetch_klines(symbol, "Min5", limit)


def get_mexc_futures_klines_15m(symbol, limit=200):
    return _fetch_klines(symbol, "Min15", limit)


def get_mexc_futures_klines_30m(symbol, limit=200):
    return _fetch_klines(symbol, "Min30", limit)


def get_mexc_futures_klines_1h(symbol, limit=200):
    return _fetch_klines(symbol, "Min60", limit)