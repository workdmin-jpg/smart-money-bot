# smart_money.py
# ===============================
# SMART MONEY CORE (v1.6)
# - CHoCH + BOS
# - Order Block
# - Multi TP (TP1 / TP2 / TP3)
# - TP3 = Liquidity + HTF (validated)
# - Safe guards added
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

    high1 = candles[-4]["high"]
    low1 = candles[-4]["low"]
    high2 = candles[-2]["high"]
    low2 = candles[-2]["low"]

    if high2 > high1 and low2 > low1:
        return "BULLISH"

    if high2 < high1 and low2 < low1:
        return "BEARISH"

    return None


def find_order_block(candles, direction):
    for i in range(len(candles) - 2, 0, -1):
        c = candles[i]

        if direction == "BULLISH" and c["close"] < c["open"]:
            return {
                "type": "BULLISH_OB",
                "high": c["high"],
                "low": c["low"],
            }

        if direction == "BEARISH" and c["close"] > c["open"]:
            return {
                "type": "BEARISH_OB",
                "high": c["high"],
                "low": c["low"],
            }

    return None


# ===============================
# SMART TARGETS
# ===============================

def find_liquidity_level(candles, direction):
    if not candles:
        return None

    try:
        return max(c["high"] for c in candles) if direction == "BUY" else min(c["low"] for c in candles)
    except:
        return None


def find_htf_level(candles, direction):
    if not candles:
        return None

    try:
        return max(c["high"] for c in candles) if direction == "BUY" else min(c["low"] for c in candles)
    except:
        return None


def build_trade(ob, direction, candles_30m, candles_1h):
    entry = (ob["high"] + ob["low"]) / 2

    if direction == "BUY":
        stop = ob["low"]
        risk = entry - stop
    else:
        stop = ob["high"]
        risk = stop - entry

    # حماية من risk صفر
    if risk <= 0:
        return None

    if direction == "BUY":
        tp1 = entry + risk
        tp2 = entry + risk * 2
    else:
        tp1 = entry - risk
        tp2 = entry - risk * 2

    # TP3 ذكي
    liquidity_tp = find_liquidity_level(candles_30m, direction)
    htf_tp = find_htf_level(candles_1h, direction)

    smart_tp3 = None
    if liquidity_tp and htf_tp:
        smart_tp3 = max(liquidity_tp, htf_tp) if direction == "BUY" else min(liquidity_tp, htf_tp)
    else:
        smart_tp3 = tp2 + risk if direction == "BUY" else tp2 - risk

    # تأكيد أن TP3 منطقي
    if direction == "BUY" and smart_tp3 <= tp2:
        smart_tp3 = tp2 + risk
    if direction == "SELL" and smart_tp3 >= tp2:
        smart_tp3 = tp2 - risk

    return {
        "entry": round(entry, 6),
        "stop": round(stop, 6),
        "tp1": round(tp1, 6),
        "tp2": round(tp2, 6),
        "tp3": round(smart_tp3, 6),
        "target": round(tp2, 6),
        "rr": "1:3",
    }


def smart_money_signal(symbol, candles_5m, candles_15m, candles_30m, candles_1h):

    choch_30m = detect_choch(candles_30m)
    bos_15m = detect_bos(candles_15m)

    if not choch_30m or not bos_15m:
        return None

    if choch_30m != bos_15m:
        return None

    ob = find_order_block(candles_5m, bos_15m)
    if not ob:
        return None

    direction = "BUY" if bos_15m == "BULLISH" else "SELL"

    trade = build_trade(ob, direction, candles_30m, candles_1h)
    if not trade:
        return None

    return {
        "symbol": symbol,
        "direction": direction,
        "entry": trade["entry"],
        "stop": trade["stop"],
        "target": trade["target"],
        "tp1": trade["tp1"],
        "tp2": trade["tp2"],
        "tp3": trade["tp3"],
        "rr": trade["rr"],
        "model": "SMC",
        "confidence": 1.0,
        "htf_bias": choch_30m,
        "order_block": ob,
    }
