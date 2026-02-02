# core/market_scanner.py
# ===============================
# MANUAL WATCHLIST (SAFE MODE)
# ===============================

def get_watchlist():
    return [
        {"symbol": "BTCUSDT", "liquidity": "MANUAL"},
        {"symbol": "ETHUSDT", "liquidity": "MANUAL"},
        {"symbol": "BNBUSDT", "liquidity": "MANUAL"},
        {"symbol": "SOLUSDT", "liquidity": "MANUAL"},
        {"symbol": "XRPUSDT", "liquidity": "MANUAL"},
    ]
