def get_watchlist():
    markets = []
    added = set()

    # ===============================
    # 1️⃣ MANUAL PAIRS FIRST
    # ===============================
    for symbol in MANUAL_PAIRS:
        if symbol not in added:
            markets.append({
                "symbol": symbol,
                "liquidity": "MANUAL"
            })
            added.add(symbol)

    # ===============================
    # 2️⃣ MARKET SCAN (REST)
    # ===============================
    try:
        market_data = fetch_markets_from_source()  # دالتك الحالية
        for m in market_data:
            symbol = m.get("symbol")
            if symbol and symbol not in added:
                markets.append(m)
                added.add(symbol)
    except Exception as e:
        print(f"⚠️ Market source failed: {e}")

    return markets
