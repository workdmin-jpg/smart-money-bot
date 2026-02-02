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

TEST_MODE = True          # True للاختبار فقط
MIN_SIGNAL_STEP = 0       # 0 أثناء الاختبار

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
    fetchers = {
        "5m": (get_binance_futures_klines_5m, get_mexc_futures_klines_5m),
        "15m": (get_binance_futures_klines_15m, get_mexc_futures_klines_15m),
        "30m": (get_binance_futures_klines_30m, get_mexc_futures_klines_30m),
        "1h": (get_binance_futures_klines_1h, get_mexc_futures_klines_1h),
    }

    for fetch in fetchers.get(tf, []):
        try:
            data = fetch(symbol)
            if isinstance(data, list) and len(data) >= 50:
                return data
        except Exception as e:
            print(f"⚠️ Fetch failed {symbol} {tf}: {e}")

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
            if isinstance(c, (list, tuple)) and len(c) >= 6:
                o, h, l, cl, v = c[1], c[2], c[3], c[4], c[5]
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
    print(f"📋 WATCHLIST SIZE: {len(watchlist) if watchlist else 0}")

    if not watchlist:
        print("❌ Watchlist empty")
        return

    for market in watchlist:
        symbol = market.get("symbol")
        source = market.get("liquidity", "MANUAL")

        if not symbol:
            continue

        try:
            r5  = futures_klines(symbol, "5m")
            r15 = futures_klines(symbol, "15m")
            r30 = futures_klines(symbol, "30m")
            r1h = futures_klines(symbol, "1h")

            if not (r5 and r15 and r30 and r1h):
                print(f"⛔ Missing klines {symbol}")
                continue

            c5  = normalize(r5)
            c15 = normalize(r15)
            c30 = normalize(r30)
            c1h = normalize(r1h)

            if not (c5 and c15 and c30 and c1h):
                print(f"⛔ Normalize failed {symbol}")
                continue

            signal = smart_money_signal(symbol, c5, c15, c30, c1h)

            if not signal:
                print(f"ℹ️ No SMC signal for {symbol}")

            # ==============================
            # TEST MODE FALLBACK
            # ==============================

            if not signal and TEST_MODE:
                last = c5[-1]["close"]
                signal = {
                    "direction": "BUY",
                    "entry": round(last, 6),
                    "stop": round(last * 0.99, 6),
                    "tp1": round(last * 1.01, 6),
                    "tp2": round(last * 1.02, 6),
                    "tp3": round(last * 1.03, 6),
                    "rr": "TEST",
                    "model": "TEST_MODE"
                }

            if not signal:
                continue

            score = calculate_signal_score(signal)
            if score < LAST_SIGNAL_SCORE.get(symbol, 0) + MIN_SIGNAL_STEP:
                continue

            LAST_SIGNAL_SCORE[symbol] = score

            message = (
                f"🚀 SMART MONEY SIGNAL\n\n"
                f"PAIR: {symbol}\n"
                f"SOURCE: {source}\n"
                f"DIRECTION: {signal['direction']}\n\n"
                f"📍 ENTRY: {signal['entry']}\n"
                f"🛑 SL: {signal['stop']}\n\n"
                f"🎯 TP1: {signal['tp1']}\n"
                f"🎯 TP2: {signal['tp2']}\n"
                f"🎯 TP3: {signal['tp3']}\n\n"
                f"RR: {signal.get('rr')}\n"
                f"MODEL: {signal.get('model')}\n\n"
                f"SCORE: {score}%\n"
                f"TIME: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
            )

            send_telegram_message(message)
            print(f"✅ SIGNAL SENT {symbol}")
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ {symbol} error: {e}")

# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    print("✅ BOT CODE LOADED SUCCESSFULLY")
    while True:
        run_bot()
        time.sleep(300)
