# context/market_context.py
# ===============================
# Unified Market Context Engine
# ===============================

from context.cmc import get_coinmarketcap_score
from context.news import get_news_score
from context.whales import get_whales_score


def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0


def analyze_market_context(symbol, days=3):
    try:
        news = safe_float(get_news_score(symbol, days))
        cmc = safe_float(get_coinmarketcap_score(symbol, days))
        whales = safe_float(get_whales_score(symbol, days))

        total = news + cmc + whales

        if total >= 70:
            status = "STRONG_MARKET_INTEREST"
        elif total >= 40:
            status = "MODERATE_MARKET_INTEREST"
        elif total > 0:
            status = "WEAK_MARKET_INTEREST"
        else:
            status = "NO_CONTEXT_SIGNAL"

        return {
            "score": total,
            "status": status,
            "details": {
                "news": news,
                "cmc": cmc,
                "whales": whales
            }
        }

    except Exception as e:
        return {
            "score": 0,
            "status": "NO_CONTEXT_SIGNAL",
            "details": {},
            "error": str(e)
        }
