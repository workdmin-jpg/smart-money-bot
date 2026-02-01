# context/context_engine.py

from context.whale_alert import analyze_whales

def build_market_context(symbol, news_context):
    whale_context = analyze_whales(symbol)

    total_score = whale_context["score"] + news_context["score"]

    if news_context["score"] == 0 and whale_context["score"] == 0:
        return {
            "label": "🚫 NO MARKET SIGNAL",
            "total_score": 0,
            "market": news_context,
            "whales": whale_context,
            "sources": []
        }

    label = "😴 Neutral Market Context"

    if total_score >= 40:
        label = "🔥 STRONG MARKET CONTEXT"
    elif total_score >= 15:
        label = "📈 BULLISH MARKET CONTEXT"
    elif total_score <= -40:
        label = "🔥 STRONG BEARISH CONTEXT"
    elif total_score <= -15:
        label = "📉 BEARISH MARKET CONTEXT"

    return {
        "label": label,
        "total_score": total_score,
        "market": news_context,
        "whales": whale_context,
        "sources": ["Whale Alert"]
    }