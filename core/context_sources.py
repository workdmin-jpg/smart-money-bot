# core/context_sources.py

import requests
from datetime import datetime, timedelta

LOOKBACK_DAYS = 3
TIME_LIMIT = datetime.utcnow() - timedelta(days=LOOKBACK_DAYS)

# ==============================
# NEWS (CryptoPanic - Free)
# ==============================

def fetch_news_score(symbol):
    try:
        coin = symbol.replace("USDT", "")
        url = f"https://cryptopanic.com/api/v1/posts/?currencies={coin}&public=true"
        r = requests.get(url, timeout=8).json()

        score = 0
        for item in r.get("results", []):
            published = datetime.fromisoformat(item["published_at"].replace("Z", ""))
            if published >= TIME_LIMIT:
                score += 5

        return min(score, 30)
    except:
        return 0


# ==============================
# COINMARKETCAP (Interest Proxy)
# ==============================

def fetch_cmc_score(symbol):
    try:
        coin = symbol.replace("USDT", "")
        # بدون API KEY – منطق ذكي
        majors = ["BTC", "ETH", "BNB", "SOL", "XRP"]
        return 20 if coin in majors else 10
    except:
        return 0


# ==============================
# WHALES (Proxy Logic)
# ==============================

def fetch_whale_score(symbol):
    try:
        coin = symbol.replace("USDT", "")
        institutional = ["BTC", "ETH", "BNB", "SOL"]
        return 20 if coin in institutional else 5
    except:
        return 0