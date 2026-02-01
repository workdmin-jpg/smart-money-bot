# core/context_sources/twitter.py

import requests
from datetime import datetime, timedelta

TWITTER_BEARER_TOKEN = "PUT_YOUR_X_BEARER_TOKEN"

HEADERS = {
    "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
}

TRUSTED_ACCOUNTS = {
    "binance": 3,
    "coinbase": 3,
    "krakenfx": 3,
    "glassnode": 2,
    "intotheblock": 2,
    "cryptoquant": 2,
    "cz_binance": 1,
    "elonmusk": 1,
}


def fetch_tweets(query, days=3):
    since = (datetime.utcnow() - timedelta(days=days)).isoformat("T") + "Z"

    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        "query": query,
        "max_results": 50,
        "tweet.fields": "created_at,author_id",
        "start_time": since
    }

    r = requests.get(url, headers=HEADERS, params=params, timeout=10)
    return r.json().get("data", [])


def analyze_twitter_sentiment(symbol):
    base = symbol.replace("USDT", "")
    tweets = fetch_tweets(base)

    if not tweets:
        return None

    score = 0
    mentions = 0

    for t in tweets:
        author = t.get("author_id")
        # في التطبيق الحقيقي نربط author_id بالـ username
        # هنا منطق مبسط
        for acc, weight in TRUSTED_ACCOUNTS.items():
            if acc.lower() in t.get("text", "").lower():
                mentions += 1
                score += weight * 5

    if mentions == 0:
        return None

    return {
        "mentions": mentions,
        "score": score
    }