# core/htf_filter.py

def get_htf_bias(candles_30m):
    if len(candles_30m) < 20:
        return None

    highs = [c[1] for c in candles_30m[-20:]]
    lows = [c[2] for c in candles_30m[-20:]]

    last_close = candles_30m[-1][3]

    if last_close > max(highs[:-1]):
        return "BULLISH"

    if last_close < min(lows[:-1]):
        return "BEARISH"

    return "RANGE"