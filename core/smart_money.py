# core/smart_money.py

def detect_breakout(candles, lookback=20, threshold=0.5):
    """
    كشف كسر هيكلي بسيط (Break of Structure)
    candles: قائمة شموع [open, high, low, close]
    """
    if len(candles) < lookback:
        return None

    recent = candles[-lookback:]
    highs = [c[1] for c in recent]
    lows = [c[2] for c in recent]

    max_high = max(highs[:-1])
    min_low = min(lows[:-1])

    last_close = recent[-1][3]

    # كسر صاعد
    if last_close > max_high * (1 + threshold / 100):
        return "BULLISH"

    # كسر هابط
    if last_close < min_low * (1 - threshold / 100):
        return "BEARISH"

    return None