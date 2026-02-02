import time
from datetime import datetime

from smart_money import smart_money_signal
from telegram_alerts import send_telegram_message
from core.market_scanner import get_watchlist
from core.market_context import calculate_market_context

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
# FUTURES FALLBACK
# ==============================

def futures_klines(symbol, tf):
    try:
        if tf == "5m":
            data = get_binance_futures_klines_5m(symbol)
        elif tf == "15m":
            data = get_binance_futures_klines_15m(symbol)
        elif tf == "30m":
            data = get_binance_futures_klines_30m(symbol)
        else:
            data = get_binance_futures_klines_1h(symbol)

        if data and len(data) > 20:
            return data
    except Exception:
        pass

    try:
        if tf == "5m":
            return get_mexc_futures_klines_5m(symbol)
        elif tf == "15m":
            return get_mexc_futures_klines_15m(symbol)
        elif tf == "30m":
            return get_mexc_futures_klines_30m(symbol)
        else:
            return get_mexc_futures_klines_1h(symbol)
    except Exception:
        return None

# ==============================
# NORMALIZE
# ==============================

def normalize(raw):
    try:
        return [{
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5]),
        } for c in raw]
    except Exception:
        return None

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
# TRADE TYPE
# ==============================

def classify_trade(context_score):
    if context_score >= 70:
        return "SWING / POSITION"
    elif context_score >= 40:
        return "INTRADAY"
    return "SCALP"

# ==============================
# MAIN LOOP
# ==============================

def run_bot():
    print("🔄 Scanning market...")
    watchlist = get_watchlist() or []

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

            context = calculate_market_context(symbol)

            score = calculate_signal_score(signal)
            last = LAST_SIGNAL_SCORE.get(symbol, 0)
            if score < last + MIN_SIGNAL_STEP:
                continue

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
                f"📡 CONTEXT: {context['status']} ({context['score']}%)\n"
                f"📰 {context['details'].get('news',0)} | "
                f"📊 {context['details'].get('cmc',0)} | "
                f"🐋 {context['details'].get('whales',0)}\n\n"
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
