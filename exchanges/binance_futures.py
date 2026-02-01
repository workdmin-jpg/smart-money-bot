import json
import urllib.request
import urllib.parse


BASE_URL = "https://fapi.binance.com/fapi/v1/klines"


def _get_klines(symbol, interval, limit=200):
    params = urllib.parse.urlencode({
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    })

    url = f"{BASE_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        raise Exception(f"Binance Futures error {symbol} {interval}: {e}")


def get_binance_futures_klines_5m(symbol, limit=200):
    return _get_klines(symbol, "5m", limit)


def get_binance_futures_klines_15m(symbol, limit=200):
    return _get_klines(symbol, "15m", limit)


def get_binance_futures_klines_30m(symbol, limit=200):
    return _get_klines(symbol, "30m", limit)


def get_binance_futures_klines_1h(symbol, limit=200):
    return _get_klines(symbol, "1h", limit)
