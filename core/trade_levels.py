def calculate_levels(signal, candles):
    last = candles[-1]
    high = last[1]
    low = last[2]
    close = last[3]

    if signal["direction"] == "BUY":
        entry = close
        stop = low
        target = entry + (entry - stop) * 4  # R:R = 1:4
    else:
        entry = close
        stop = high
        target = entry - (stop - entry) * 4

    return {
        "entry": round(entry, 6),
        "stop_loss": round(stop, 6),
        "target": round(target, 6),
        "rr": "1:4"
    }