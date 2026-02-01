# core/signal_engine.py

def generate_signal(symbol, candles, liquidity):
    """
    إنشاء إشارة تداول آمنة للمبتدئ
    """
    if liquidity != "HIGH":
        return None

    if len(candles) < 20:
        return None

    highs = [c[1] for c in candles[-20:]]
    lows = [c[2] for c in candles[-20:]]

    last = candles[-1]
    prev = candles[-2]

    max_high = max(highs[:-1])
    min_low = min(lows[:-1])

    # إشارة شراء (كسر صاعد)
    if last[3] > max_high:
        entry = last[3]
        stop = min_low
        target = entry + (entry - stop)  # RR = 1:1

        return {
            "symbol": symbol,
            "direction": "BUY",
            "entry": round(entry, 4),
            "stop_loss": round(stop, 4),
            "target": round(target, 4),
            "risk_reward": "1:1"
        }

    # إشارة بيع (كسر هابط)
    if last[3] < min_low:
        entry = last[3]
        stop = max_high
        target = entry - (stop - entry)

        return {
            "symbol": symbol,
            "direction": "SELL",
            "entry": round(entry, 4),
            "stop_loss": round(stop, 4),
            "target": round(target, 4),
            "risk_reward": "1:1"
        }

    return None