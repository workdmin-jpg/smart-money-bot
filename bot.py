import time
from datetime import datetime

from core.manual_watchlist import get_watchlist
from smart_money import smart_money_signal
from telegram_alerts import send_telegram_message

from exchanges.binance_futures import (
    get_binance_futures_klines_5m,
    get_binance_futures_klines_15m,
    get_binance_futures_klines_30m,
    get_binance_futures_klines_1h,
)

from exchanges.mexc_futures import (
    get_mexc_futures_klines_5m,
    get_mexc_futures_klines_15m,
    get_mexc_futures_klines_30m,
    get_mexc_futures_klines_1h,
)

# ==============================
# SETTINGS
# ==============================

TEST_MODE = True
MIN_SIGNAL_STEP = 0

LAST_SIGNAL_SCORE = {}

# ==============================
# HELPERS
# ==============================

def safe_float(v):
    try:
        return float(v)
    except:
        return None

# ==============================
# DATA FETCH
# ==============================

def futures_klines(symbol, tf):
    for source in ("binance", "mexc"):
        try:
            fetch = {
                "binance": {
                    "5m": get_binance_futures_klines_5m,
                    "15m": get_binance_futures_klines_15m,
                    "30m": get_binance_futures_klines_30m,
                    "1h": get_binance_futures_klines_1h,
                },
                "mexc": {
                    "5m": get_mexc_futures_klines_5m,
                    "15m": get_mexc_futures_klines_15m,
                    "30m": get_mexc_futures_klines_30m,
                    "1h": get_mexc_futures_klines_1h,
                },
            }[source][tf]

            data = fetch(symbol)
            if isinstance(data, list) and len(data) >= 20:
                return data
        except:
            continue

    return None

# ==============================
# NORMALIZE
# ==============================

def normalize(raw):
    candles = []
    if not isinstance(raw, list):
        return None

    for c in raw:
        o, h, l, cl, v = map(safe_float, c[1:6])
        if None in (o, h, l, cl, v):
            continue

        candles.append({
            "open": o,
            "high": h,
            "low": l,
            "close": cl,
            "volume": v,
        })

    return candles if len(candles) >= 20 else None

# ==============================
# SCORE
# ==============================

def calculate_signal_score(signal):
    score = 50
    if signal.get("rr"):
        score += 10
    if signal.get("model"):
        score += 10
    return min(score, 100)

# ==============================
# MAIN LOOP
# ==============================

def run_bot():
    print("🔄 Scanning market...")

    watchlist = get_watchlist()
    if not watchlist:
        print("❌ Watchlist empty")
        return

    for market in watchlist:
        symbol = market.get("symbol")
        if not symbol:
            continue

        r5 = futures_klines(symbol, "5m")
        r15 = futures_klines(symbol, "15m")
        r30 = futures_klines(symbol, "30m")
        r1h = futures_klines(symbol, "1h")

        if not all([r5, r15, r30, r1h]):
            continue

        c5, c15, c30, c1h = map(normalize, [r5, r15, r30, r1h])
        if not all([c5, c15, c30, c1h]):
            continue

        signal = smart_money_signal(symbol, c5, c15, c30, c1h)

        if not signal and TEST_MODE:
            last = c5[-1]["close"]
            signal = {
                "direction": "LONG",
                "entry": last,
                "stop": last * 0.99,
                "tp1": last * 1.01,
                "tp2": last * 1.02,
                "tp3": last * 1.03,
                "rr": "TEST",
                "model": "TEST_MODE",
            }

        if not signal:
            continue

        score = calculate_signal_score(signal)
        if score < LAST_SIGNAL_SCORE.get(symbol, 0) + MIN_SIGNAL_STEP:
            continue
