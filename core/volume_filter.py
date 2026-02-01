def volume_spike(candles):
    if len(candles) < 20:
        return False

    volumes = [c[4] for c in candles[-20:]]
    last_volume = volumes[-1]
    avg_volume = sum(volumes[:-1]) / len(volumes[:-1])

    return last_volume > avg_volume * 1.8