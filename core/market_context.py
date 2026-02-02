# context/market_context.py
# ===============================
# Unified Market Context Engine (SAFE MODE)
# ===============================

from context.cmc import get_coinmarketcap_score
from context.news import get_news_score
from context.whales import get_whales_score


def _safe_score(value):
    try:
        return max(float(value), 0)
    except:
        return 0


def analyze_market_context(symbol, days=3):
    news = _safe_score(get_news_score(symbol, days))
    cmc = _safe_score(get_coinmarketcap_score(symbol, days))
    whales = _safe_score(get_whales_score(symbol, days))

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
