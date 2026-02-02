# smart_money.py
# ===============================
# SMART MONEY CORE (v1.6 FIXED)
# ===============================

def detect_bos(candles):
    if len(candles) < 3:
        return None

    last = candles[-1]
    prev = candles[-2]

    if last["close"] > prev["high"]:
        return "BULLISH"
    if last["close"] < prev["low"]:
        return "BEARISH"

    return None


def detect_choch(candles):
    if len(candles) < 4:
        return None

    h1, l1 = candles[-4]["high"], candles[-4]["low"]
    h2, l2 = candles[-2]["high"], candles[-2]["low"]

    if h2 > h1 and l2 > l1:
        return "BULLISH"
    if h2 < h1 and l2 < l1:
        return "BEARISH"

    return None


def find_order_block(candles, direction):
    # نبحث عن آخر شمعة معاكسة قبل الحركة
    for i in range(len(candles) - 3, 1, -1):
        c = candles[i]

        if direction == "BULLISH" and c["close"] < c["open"]:
            return {"high": c["high"], "low": c["low"]}

        if direction == "BEARISH" and c["close"] > c["open"]:
            return {"high": c["high"], "low": c["low"]}

    # fallback: آخر نطاق
    last = candles[-2]
    return {"high": last["high"], "low": last["low"]}


def build_trade(ob, direction, candles_30m, candles_1h):
    entry = (ob["high"] + ob["low"]) / 2

    if direction == "BUY":
        stop = ob["low"]
        risk = entry - stop
        tp1 = entry + risk
        tp2 = entry + risk * 2
        tp3 = max(c["high"] for c in candles_1h)
    else:
        stop = ob["high"]
        risk = stop - entry
        tp1 = entry - risk
        tp2 = entry - risk * 2
        tp3 = min(c["low"] for c in candles_1h)

    if risk <= 0:
        return None

    return {
        "entry": round(entry, 6),
        "stop": round(stop, 6),
        "tp1": round(tp1, 6),
        "tp2": round(tp2, 6),
        "tp3": round(tp3, 6),
        "target": round(tp2, 6),
        "rr": "1:2+",
    }


def smart_money_signal(symbol, candles_5m, candles_15m, candles_30m, candles_1h):

    bos = detect_bos(candles_15m)
    choch = detect_choch(candles_30m)

    # سماح ذكي
    direction_bias = bos or choch
    if not direction_bias:
        return None

    direction = "BUY" if direction_bias == "BULLISH" else "SELL"

    ob = find_order_block(candles_5m, direction_bias)
    if not ob:
        return None

    trade = build_trade(ob, direction, candles_30m, candles_1h)
    if not trade:
        return None

    return {
        "symbol": symbol,
        "direction": direction,
        **trade,
        "model": "SMC",
        "confidence": 0.85,
