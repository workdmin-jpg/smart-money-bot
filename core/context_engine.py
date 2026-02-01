# core/context_engine.py

def build_context_report(
    symbol,
    market_context,
    whale_context,
    influencer_context,
    sources=None
):
    """
    دمج السياق النهائي – مستقل تمامًا عن التداول
    """

    if sources is None:
        sources = []

    # ==============================
    # NO MARKET SIGNAL (قاعدة صارمة)
    # ==============================
    if (
        market_context.get("label", "").startswith("🚫")
        and whale_context.get("label", "").startswith("🚫")
        and influencer_context.get("label", "").startswith("🚫")
    ):
        return {
            "symbol": symbol,
            "total_score": 0,
            "label": "🚫 NO MARKET SIGNAL",
            "details": "No market/news/whale/influencer activity in last 3 days",
            "market": market_context,
            "whales": whale_context,
            "influencers": influencer_context,
            "sources": sources
        }

    # ==============================
    # SCORE CALCULATION
    # ==============================
    total_score = (
        market_context.get("score", 0) +
        whale_context.get("score", 0) +
        influencer_context.get("score", 0)
    )

    # ==============================
    # FINAL LABEL
    # ==============================
    if total_score >= 70:
        label = "🔥 STRONG MARKET CONTEXT"
    elif total_score >= 35:
        label = "📈 BULLISH MARKET CONTEXT"
    elif total_score <= -35:
        label = "📉 BEARISH MARKET CONTEXT"
    else:
        label = "😴 NEUTRAL MARKET CONTEXT"

    return {
        "symbol": symbol,
        "total_score": int(total_score),
        "label": label,
        "market": market_context,
        "whales": whale_context,
        "influencers": influencer_context,
        "sources": sources
    }