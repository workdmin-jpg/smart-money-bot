import json
import ssl
import urllib.request
import urllib.parse

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://api.binance.com"


def get_klines(symbol, interval="5m", limit=100):
    params = urllib.parse.urlencode({
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    })

    url = f"{BASE_URL}/api/v3/klines?{params}"

    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode())


# ==============================
# دوال توافق (حتى لا نغيّر bot.py)
# ==============================

def get_klines_5m(symbol, limit=100):
    return get_klines(symbol, "5m", limit)


def get_klines_15m(symbol, limit=100):
    return get_klines(symbol, "15m", limit)


def get_klines_30m(symbol, limit=100):
    return get_klines(symbol, "30m", limit)


def get_klines_1h(symbol, limit=100):
    return get_klines(symbol, "1h", limit)
# ==============================
# Compatibility aliases
# ==============================

def get_binance_klines_5m(symbol, limit=100):
    return get_klines(symbol, "5m", limit)


def get_binance_klines_15m(symbol, limit=100):
    return get_klines(symbol, "15m", limit)


def get_binance_klines_30m(symbol, limit=100):
    return get_klines(symbol, "30m", limit)


def get_binance_klines_1h(symbol, limit=100):
    return get_klines(symbol, "1h", limit)