def near_signal(candles):
    if len(candles) < 20:
        return False

    highs = [c[1] for c in candles[-20:]]
    lows = [c[2] for c in candles[-20:]]

    last_close = candles[-1][3]

    if last_close > max(highs[:-1]) * 0.995:
        return "BUY"

    if last_close < min(lows[:-1]) * 1.005:
        return "SELL"

    return False