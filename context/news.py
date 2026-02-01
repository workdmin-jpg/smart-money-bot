# context/news.py
# ===============================
# News Context Score
# ===============================

import json
import urllib.request
from datetime import datetime, timedelta

from settings import NEWS_API_KEY


NEWS_URL = "https://newsapi.org/v2/everything"


def get_news_score(symbol, days=3):
    """
    Returns score 0–30 based on:
    - number of news articles
    - recency (last X days)
    """

    if not NEWS_API_KEY:
        return 0

    base_symbol = symbol.replace("USDT", "")
    from_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")

    params = (
        f"?q={base_symbol}"
        f"&from={from_date}"
        f"&sortBy=publishedAt"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:
        with urllib.request.urlopen(NEWS_URL + params, timeout=10) as r:
            data = json.loads(r.read().decode())

        articles = data.get("articles", [])
        count = len(articles)

        if count >= 10:
            return 30
        elif count >= 5:
            return 20
        elif count >= 1:
            return 10

        return 0

    except Exception as e:
        print(f"NEWS ERROR {symbol}: {e}")
        return 0