# core/context_influencers.py

import time

MAX_AGE_SECONDS = 3 * 24 * 60 * 60  # 72 ساعة

def influencer_sentiment_score(posts):
    """
    posts = [
        {
            "sentiment": "bullish" | "bearish",
            "weight": 1.0,   # حساب موثوق = وزن أعلى
            "timestamp": unix_time
        }
    ]
    """

    if not posts:
        return {
            "score": 0,
            "label": "🚫 NO MARKET SIGNAL",
            "reason": "No influencer activity in last 72h"
        }

    now = time.time()
    score = 0
    bulls = 0
    bears = 0

    for p in posts:
        if now - p["timestamp"] > MAX_AGE_SECONDS:
            continue

        if p["sentiment"] == "bullish":
            bulls += 1
            score += 10 * p.get("weight", 1)

        elif p["sentiment"] == "bearish":
            bears += 1
            score -= 10 * p.get("weight", 1)

    if bulls == 0 and bears == 0:
        return {
            "score": 0,
            "label": "🚫 NO MARKET SIGNAL",
            "reason": "No recent influencer posts"
        }

    if score >= 25:
        label = "👥 Strong Bullish Sentiment"
    elif score <= -25:
        label = "👥 Strong Bearish Sentiment"
    else:
        label = "👥 Mixed Influencer Sentiment"

    return {
        "score": int(max(min(score, 30), -30)),
        "label": label,
        "bullish": bulls,
        "bearish": bears
    }