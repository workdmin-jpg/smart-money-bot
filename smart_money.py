# smart_money.py

def smart_money_signal(symbol, c5, c15, c30, c1h):
    """
    Simple Smart Money placeholder
    Prevents syntax errors and keeps bot running
    """

    try:
        # basic validation
        if not (c5 and c15 and c30 and c1h):
            return None

        last_close = c5[-1]["close"]
        prev_close = c5[-2]["close"]

        # very simple logic (can be expanded لاحقًا)
        if last_close > prev_close:
            direction = "BUY"
            entry = last_close
            stop = round(entry * 0.99, 6)
            tp1 = round(entry * 1.01, 6)
            tp2 = round(entry * 1.02, 6)
            tp3 = round(entry * 1.03, 6)
        else:
            direction = "SELL"
            entry = last_close
            stop = round(entry * 1.01, 6)
            tp1 = round(entry * 0.99, 6)
            tp2 = round(entry * 0.98, 6)
            tp3 = round(entry * 0.97, 6)

        return {
            "direction": direction,
            "entry": entry,
            "stop": stop,
            "tp1": tp1,
            "tp2": tp2,
            "tp3": tp3,
            "rr": "AUTO",
            "model": "SIMPLE_SMC"
        }

    except Exception as e:
        print(f"SMC ERROR {symbol}: {e}")
        return None
