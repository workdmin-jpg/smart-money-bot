# core/context_cmc.py

import time
import json
import urllib.request
import urllib.parse

CMC_API_KEY = "PUT_YOUR_CMC_API_KEY_HERE"

BASE_URL = "https://pro-api.coinmarketcap.com/v1"
MAX_AGE_SECONDS = 3 * 24 * 60 * 60  # 72 ساعة


def _request(endpoint, params=None):
    if params is None:
        params = {}

    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{endpoint}?{query}"

    req = urllib.request.Request(
        url,
        headers={
            "X-CMC_PRO_API_KEY": CMC_API_KEY,
            "Accept": "application/json"
        }
    )

    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode())


# ==============================
# TRENDING COINS
# ==============================

def is_trending(symbol):
    try:
        data = _request("/cryptocurrency/trending/latest")
        coins = data.get("data", [])

        symbols = [c["symbol"] for c in coins]
        return symbol.replace("USDT", "") in symbols

    except Exception:
        return False


# ==============================
# NEWS (LAST 72H ONLY)
# ==============================

def get_recent_news(symbol):
    """
    نعيد قائمة أخبار خلال آخر 72 ساعة فقط
    """
    try:
        data = _request(
            "/content/latest",
            {
                "symbol": symbol.replace("USDT", ""),
                "limit": 20
            }
        )

        now = time.time()
        news_items = []

        for item in data.get("data", []):
            published = item.get("published_at")

            if not published:
                continue

            # تحويل ISO → timestamp
            ts = int(time.mktime(time.strptime(
                published.split(".")[0],
                "%Y-%m-%dT%H:%M:%S"
            )))

            if now - ts > MAX_AGE_SECONDS:
                continue

            sentiment = "neutral"
            title = item.get("title", "").lower()

            if any(k in title for k in ["partnership", "adoption", "bull", "institution"]):
                sentiment = "positive"
            elif any(k in title for k in ["hack", "lawsuit", "dump", "bear"]):
                sentiment = "negative"

            news_items.append({
                "title": item.get("title"),
                "sentiment": sentiment,
                "timestamp": ts
            })

        return news_items

    except Exception:
        return []