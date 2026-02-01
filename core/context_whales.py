# core/context_whales.py

import time

MAX_AGE_SECONDS = 3 * 24 * 60 * 60  # 72 ساعة

def whale_activity_score(events):
    """
    events = [
        {
            "type": "accumulation" | "distribution",
            "amount_usdt": 8000000,
            "timestamp": unix_time
        }
    ]
    """

    if not events:
        return {
            "score": 0,
            "label": "🚫 NO MARKET SIGNAL",
            "reason": "No whale activity in last 72h"
        }

    now = time.time()
    score = 0
    acc = 0
    dist = 0

    for e in events:
        if now - e["timestamp"] > MAX_AGE_SECONDS:
            continue

        if e["type"] == "accumulation":
            acc += 1
            score += min(e["amount_usdt"] / 1_000_000 * 5, 25)

        elif e["type"] == "distribution":
            dist += 1
            score -= min(e["amount_usdt"] / 1_000_000 * 5, 25)

    if acc == 0 and dist == 0:
        return {
            "score": 0,
            "label": "🚫 NO MARKET SIGNAL",
            "reason": "No recent whale events"
        }

    if score >= 30:
        label = "🐋 Strong Accumulation"
    elif score <= -30:
        label = "🐋 Strong Distribution"
    else:
        label = "🐋 Mixed Whale Activity"

    return {
        "score": int(max(min(score, 40), -40)),
        "label": label,
        "accumulations": acc,
        "distributions": dist
    }