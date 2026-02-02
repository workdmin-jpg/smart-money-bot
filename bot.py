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

TEST_MODE = True        # اجعله True فقط للاختبار
MIN_SIGNAL_STEP = 0

# ==============================
# MEMORY
# ==============================

LAST_SIGNAL_SCORE = {}

# ==============================
# HELPERS
# ==============================

def safe_float(v):
    try:
        return float(v)
    except:
        return 0.0

# ==============================
# FUTURES FETCH
# ==============================

def futures_klines(symbol, tf):
    try:
        binance = {
            "5m": get_binance_futures_klines_5m,
            "15m": get_binance_futures_klines_15m,
            "30m": get_binance_futures_klines_30m,
            "1h": get_binance_futures_klines_1h,
        }
        data = binance[tf](symbol)
        if isinstance(data, list) and len(data) >= 50:
            return data
    except Exception as e:
        print(f"⚠️ Binance failed {symbol} {tf}: {e}")

    try:
        mexc = {
            "5m": get_mexc_futures_klines_5m,
            "15m": get_mexc_futures_klines_15m,
            "30m": get_mexc_futures_klines_30m,
            "1h": get_mexc_futures_klines_1h,
        }
        data = mexc[tf](symbol)
        if isinstance(data, list) and len(data) >= 50:
            return data
    except Exception as e:
        print(f"⚠️ MEXC failed {symbol} {tf}: {e}")

    return None

# ==============================
# NORMALIZE
# ==============================

def normalize(raw):
    candles = []

    if not isinstance(raw, list):
        return None

    for c in raw:
        try:
            # صيغة list
            if isinstance(c, (list, tuple)):
                o, h, l, cl, v = c[1], c[2], c[3], c[4], c[5]

            # صيغة dict
            elif isinstance(c, dict):
                o = c.get("open") or c.get("o")
                h = c.get("high") or c.get("h")
                l = c.get("low") or c.get("l")
                cl = c.get("close") or c.get("c")
                v = c.get("volume") or c.get("v")
            else:
                continue

            candles.append({
                "open": safe_float(o),
                "high": safe_float(h),
                "low": safe_float(l),
                "close": safe_float(cl),
                "volume": safe_float(v),
            })
        except:
            continue

    return candles if len(candles) >= 20 else None
# ==============================
# SCORE
# ==============================

def calculate_signal_score(signal):
    score = 50
    if signal.get("rr"):
        score += 20
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

        try:
            r5  = futures_klines(symbol, "5m")
            r15 = futures_klines(symbol, "15m")
            r30 = futures_klines(symbol, "30m")
            r1h = futures_klines(symbol, "1h")

           if not r5 or not r15 or not r30 or not r1h:
    continue                                                                
]
