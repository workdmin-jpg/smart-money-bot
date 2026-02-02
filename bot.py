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

TEST_MODE = True          # يسمح بإرسال إشارات تجريبية
MIN_SIGNAL_STEP = 0       # أثناء الاختبار (نرفعه لاحقًا)

# ==============================
# MEMORY (ANTI DUPLICATION)
# ==============================

LAST_SIGNAL_SCORE = {}

# ==============================
# SAFE HELPERS
# ==============================

def safe_float(v):
    try:
        return float(v)
    except:
        return 0.0

# ==============================
# SAFE FUTURES FETCH
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
        if isinstance(data, list) and len(data) > 20:
            return data
    except:
        pass

    try:
        mexc = {
            "5m": get_mexc_futures_klines_5m,
            "15m": get_mexc_futures_klines_15m,
            "30m": get_mexc_futures_klines_30m,
            "1h": get_mexc_futures_klines_1h,
        }
        data = mexc[tf](symbol)
        if isinstance(data, list) and len(data) > 20:
            return data
    except:
        pass

    return None

# ==============================
# NORMALIZE CANDLES
# ==============================

def normalize(raw):
    candles = []
    if not isinstance(raw, list):
        return None

    for c in raw:
        try:
            candles.append({
                "open": safe_float(c[1]),
                "high": safe_float(c[2]),
                "low": safe_float(c[3]),
                "close": safe_float(c[4]),
                "volume": safe_float(c[5]),
            })
        except:
            continue

    return candles if len(candles) >= 20 else None

# ==============================
# SIGNAL SCORE
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

    try:
        watchlist = get_watchlist()
    except Exception as e:
        print(f"❌ Watchlist error: {e}")
        return

    for market in watchlist:
        symbol = market.get("symbol")
        source = market.get("liquidity", "MANUAL")

        if not symbol:
            continue

        try:
            r5 = futures_klines(symbol, "5m")
            r15 = futures_klines(symbol, "15m")
            r30 = futures_klines(symbol, "30m")
            r1h = futures_klines(symbol, "1h")

            if not all([r5, r15, r30, r1h]):
                continue

            c5, c15, c30, c1h = map(normalize, [r5, r15, r30, r1h])
            if not all([c5, c15, c30, c1h]):
                continue

            # ==============================
            # SMART MONEY SIGNAL
            # ==============================

            signal = smart_money_signal(symbol, c5, c15, c30, c1h)

            # LOG مهم
            if not signal:
                print(f"ℹ️ No Smart Money signal for {symbol}")

            # ==============================
            # TEST MODE FALLBACK
            # ==============================

            if not signal and TEST_MODE:
                last = c5[-1]["close"]
                signal = {
                    "direction": "LONG",
                    "entry": last,
                    "stop": last * 0.99,
                    "tp1": last * 1.01,
                    "tp2": last * 1.02,
                    "tp3": last * 1.03,
                    "rr": 2,
                    "model": "TEST_MODE"
                }

            if not signal:
                continue

            score = calculate_signal_score(signal)
            if score < LAST_SIGNAL_SCORE.get(symbol, 0) + MIN_SIGNAL_STEP:
                continue

            LAST_SIGNAL_SCORE[symbol] = score

            # ==============================
            # SEND TELEGRAM
            # ==============================

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
            time.sleep(0.3)

        except Exception as e:
            print(f"⛔ {symbol} error: {e}")

# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    while True:
        run_bot()
        time.sleep(300)
