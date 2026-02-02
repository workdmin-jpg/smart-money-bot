import time

from datetime import datetime
from core.manual_watchlist import get_watchlist
from smart_money import smart_money_signal
from telegram_alerts import send_telegram_message


from core.market_context import (
    get_news_score,
    get_coinmarketcap_score,
    get_whales_score,
)

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
# MEMORY (ANTI DUPLICATION)
# ==============================

LAST_SIGNAL_SCORE = {}
MIN_SIGNAL_STEP = 10

# ==============================
# SAFE HELPERS
# ==============================

def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0

# ==============================
# SAFE FUTURES FETCH
# ==============================

def futures_klines(symbol, tf):
    try:
        fetchers = {
            "5m": get_binance_futures_klines_5m,
            "15m": get_binance_futures_klines_15m,
            "30m": get_binance_futures_klines_30m,
            "1h": get_binance_futures_klines_1h,
        }
        data = fetchers[tf](symbol)
        if isinstance(data, list) and len(data) > 20:
            return data
    except:
        pass

    try:
        fetchers = {
            "5m": get_mexc_futures_klines_5m,
            "15m": get_mexc_futures_klines_15m,
            "30m": get_mexc_futures_klines_30m,
            "1h": get_mexc_futures_klines_1h,
        }
        data = fetchers[tf](symbol)
        if isinstance(data, list) and len(data) > 20:
            return data
    except:
        pass

    return None

# ==============================
# SAFE NORMALIZE
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
# MARKET CONTEXT (ULTRA SAFE)
# ==============================

def calculate_market_context(symbol):
    try:
        news = safe_float(get_news_score(symbol, 3))
        cmc = safe_float(get_coinmarketcap_score(symbol, 3))
        whales = safe_float(get_whales_score(symbol, 3))
    except:
        return {"score": 0, "status": "DISABLED", "details": {}}

    total = news + cmc + whales

    status = (
        "STRONG_MARKET_INTEREST" if total >= 70 else
        "MODERATE_MARKET_INTEREST" if total >= 40 else
        "WEAK_MARKET_INTEREST" if total > 0 else
        "NO_CONTEXT_SIGNAL"
    )

    return {
        "score": total,
        "status": status,
        "details": {"news": news, "cmc": cmc, "whales": whales},
    }

# ==============================
# TRADE TYPE
# ==============================

def classify_trade(score):
    if score >= 70:
        return "SWING / POSITION"
    elif score >= 40:
        return "INTRADAY"
    return "SCALP"

# ==============================
# MAIN LOOP
# ==============================

def run_bot():
    print("🔄 Scanning market...")

    try:
        watchlist = get_watchlist()
    except Exception as e:
        print(f"❌ Watchlist failed: {e}")
        return

    for market in watchlist:
        symbol = market.get("symbol")
        source = market.get("liquidity", "MARKET")
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

            signal = smart_money_signal(symbol, c5, c15, c30, c1h)
            if not signal:
                continue

            score = calculate_signal_score(signal)
            if score < LAST_SIGNAL_SCORE.get(symbol, 0) + MIN_SIGNAL_STEP:
                continue

            context = calculate_market_context(symbol)
            LAST_SIGNAL_SCORE[symbol] = score
            trade_type = classify_trade(context["score"])

            message = (
                f"🚀 SMART MONEY SIGNAL\n\n"
                f"PAIR: {symbol}\n"
                f"SOURCE: {source}\n"
                f"DIRECTION: {signal['direction']}\n"
                f"TYPE: {trade_type}\n\n"
                f"📍 ENTRY: {signal['entry']}\n"
                f"🛑 SL: {signal['stop']}\n\n"
                f"🎯 TP1: {signal.get('tp1')}\n"
                f"🎯 TP2: {signal.get('tp2')}\n"
                f"🎯 TP3: {signal.get('tp3')}\n\n"
                f"RR: {signal.get('rr')}\n\n"
                f"📡 CONTEXT: {context['status']} ({context['score']}%)\n\n"
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

