import json
import urllib.request
import urllib.parse

BASE_URL = "https://contract.mexc.com"

# ==============================
# CORE FUTURES KLINES
# ==============================

def get_futures_klines(symbol, interval="5m", limit=100):
    params = urllib.parse.urlencode({
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    })

    url = f"{BASE_URL}/api/v1/contract/kline?{params}"

    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode())

    return data.get("data", [])


# ==============================
# BOT COMPATIBLE FUNCTIONS
# ==============================

def get_mexc_futures_klines_5m(symbol, limit=100):
    return get_futures_klines(symbol, "5m", limit)

def get_mexc_futures_klines_15m(symbol, limit=100):
    return get_futures_klines(symbol, "15m", limit)

def get_mexc_futures_klines_30m(symbol, limit=100):
    return get_futures_klines(symbol, "30m", limit)

def get_mexc_futures_klines_1h(symbol, limit=100):
    return get_futures_klines(symbol, "1h", limit)