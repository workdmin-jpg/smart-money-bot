# core/market_context.py
# ===============================
# SAFE MARKET CONTEXT (NO APIs)
# ===============================

def calculate_market_context(candles_1h, direction):
    if not candles_1h or len(candles_1h) < 20:
        return {
            "score": 0,
            "status": "NO_DATA",
            "details": {}
        }

    volumes = [c["volume"] for c in candles_1h[-20:]]
    closes = [c["close"] for c in candles_1h[-20:]]

    avg_volume = sum(volumes) / len(volumes)
    last_volume = volumes[-1]

    # =========================
    # VOLUME SCORE (0–40)
    # =========================
    volume_score = 0
    if last_volume > avg_volume * 1.5:
        volume_score = 40
    elif last_volume > avg_volume:
        volume_score = 25
    elif last_volume > avg_volume * 0.7:
        volume_score = 10

    # =========================
    # VOLATILITY SCORE (0–30)
    # =========================
    ranges = [
        candles_1h[i]["high"] - candles_1h[i]["low"]
        for i in range(-10, -1)
    ]
    avg_range = sum(ranges) / len(ranges)
    last_range = candles_1h[-1]["high"] - candles_1h[-1]["low"]

    volatility_score = 0
    if last_range > avg_range * 1.5:
