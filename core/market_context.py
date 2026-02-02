# core/market_context.py
# ===============================
# SAFE MARKET CONTEXT ENGINE
# ===============================

def calculate_market_context(symbol, days=3):
    """
    Safe fallback context.
    External APIs disabled on Railway.
    """

    return {
        "score": 0,
        "status": "DISABLED",
        "details": {
            "news": 0,
            "cmc": 0,
            "whales": 0
        }
    }
