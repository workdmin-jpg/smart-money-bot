# smart_money.py
# SMART MONEY CORE – RELAXED v1.6

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

    h1 = candles[-4]["high"]
    l1 = candles[-4]["low"]
    h2 = candles[-2]["high"]
    l2 = candles[-2]["low"]

    if h2 > h1 and l2 > l1:
        return "BULLISH"
    if h2 < h1 and l2 < l1:
        return "BEARISH"
    return None


def find_order_block(candles, direction, lookback=7):
    for i in range(len(candles
