# smart_money.py
# ===============================
# SMART MONEY CORE (v1.5 + DEBUG)
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
            return {"high": c["high"], "low": c["low"]}

        if direction == "BEARISH" and c["close"] > c["open"]:
            return {"high": c["high"], "low": c["low"]}

    return None


def build_trade(ob, direction, candles_30m, candles_1h):
    entry = (ob["high"] + ob["low"]) / 2

    if direction == "BUY":
        stop = ob["low"]
        risk = entry - stop
        tp1 = entry + risk
        tp2 = entry + risk * 2
    else:
        stop = ob["high"]
        risk = stop - entry
        tp1 = entry - risk
        tp2 = entry - risk * 2

    tp3 = (
        max(c["high"] for c in candles_1h)
        if direction == "BUY"
        else min(c["low"] for c in candles_1h)
    )

    return {
        "entry": round(entry, 6),
        "stop": round(stop, 6),
        "tp1": round(tp1, 6),
        "tp2": round(tp2, 6),
        "tp3": round(tp3, 6),
        "target": round(tp2, 6),
        "rr": "1:3",
    }


def smart_money_signal(symbol, candles_5m, candles_15m, candles_30m, candles_1h):

    choch_30m = detect_choch(candles_30m)
    bos_15m = detect_bos(candles_15m)

    if not choch_30m:
        print(f"[SMC DEBUG] {symbol} ❌ NO CHoCH 30m")
        return None

    if not bos_15m:
        print(f"[SMC DEBUG] {symbol} ❌ NO BOS 15m")
        return None

    if choch_30m != bos_15m:
        print(f"[SMC DEBUG] {symbol} ❌ CHoCH/BOS mismatch")
        return None

    ob = find_order_block(candles_5m, bos_15m)
    if not ob:
        print(f"[SMC DEBUG] {symbol} ❌ NO Order Block 5m")
        return None

    direction = "BUY" if bos_15m == "BULLISH" else "SELL"
    trade = build_trade(ob, direction, candles_30m, candles_1h)

    print(f"[SMC DEBUG] {symbol} ✅ VALID SETUP")

    return {
        "symbol": symbol,
        "direction": direction,
        "entry": trade["entry"],
        "stop": trade["stop"],
        "tp1": trade["tp1"],
        "tp2": trade["tp2"],
        "tp3": trade["tp3"],
        "target": trade["target"],
        "rr": trade["rr"],
        "model": "SMC",
    }
