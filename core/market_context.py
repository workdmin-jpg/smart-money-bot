# core/market_context.py
# ===============================
# Unified Market Context Engine (SAFE MODE)
# ===============================

from context.cmc import get_coinmarketcap_score
from context.news import get_news_score
from context.whales import get_whales_score


def safe_score(func, symbol, days):
    try:
        value = func(symbol, days)
        if value is None:
            return 0
        return float(value)
    except:
        return 0


def calculate_market_context(symbol, days=3):
    news = safe_score(get_news_score, symbol, days)
    cmc = safe_score(get_coinmarketcap_score, symbol, days)
    whales = safe_score(get_whales_score, symbol, days)

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
        "score": int(total),
        "status": status,
        "details": {
            "news": int(news),
            "cmc": int(cmc),
            "whales": int(whales),
        },
    }
