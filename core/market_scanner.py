# core/market_scanner.py

from exchanges.binance import get_binance_spot_usdt
from exchanges.okx import get_okx_spot_usdt
from exchanges.bybit import get_bybit_spot_usdt
from exchanges.kucoin import get_kucoin_spot_usdt
from exchanges.gateio import get_gateio_spot_usdt
from exchanges.bitget import get_bitget_spot_usdt
from exchanges.mexc import get_mexc_spot_usdt

from filters.liquidity import classify_liquidity
from settings import MODE, LIQUIDITY_A, LIQUIDITY_B, CUSTOM_SYMBOLS


def _normalize_symbol(symbol: str) -> str:
    return symbol.replace("-", "").replace("_", "").upper()


def get_all_markets():
    markets = []

    sources = [
        get_binance_spot_usdt,
        get_okx_spot_usdt,
        get_bybit_spot_usdt,
        get_kucoin_spot_usdt,
        get_gateio_spot_usdt,
        get_bitget_spot_usdt,
        get_mexc_spot_usdt,
    ]

    for source in sources:
        try:
            markets.extend(source())
        except Exception as e:
            print(f"⚠️ Market source failed: {e}")

    return markets


def filter_and_merge_markets():
    raw_markets = get_all_markets()
    merged = {}

    for m in raw_markets:
        symbol = _normalize_symbol(m["symbol"])
        volume = float(m.get("volume", 0))

        if volume <= 0:
            continue

        liquidity = classify_liquidity(volume)
        if liquidity == "DEAD":
            continue

        if symbol not in merged or volume > merged[symbol]["volume"]:
            merged[symbol] = {
                "symbol": symbol,
                "volume": volume,
                "liquidity": liquidity
            }

    allowed_liquidity = LIQUIDITY_A if MODE == "A" else LIQUIDITY_B

    final_markets = [
        m for m in merged.values()
        if m["liquidity"] in allowed_liquidity
    ]

    final_markets.sort(key=lambda x: x["volume"], reverse=True)
    return final_markets


def get_watchlist(limit: int = 200):
    """
    - عملاتك أولاً
    - ثم السوق
    - بدون تكرار
    """

    watchlist = []
    seen = set()

    # 1️⃣ العملات المخصصة (أولوية)
    for sym in CUSTOM_SYMBOLS:
        symbol = _normalize_symbol(sym)
        if symbol not in seen:
            watchlist.append({
                "symbol": symbol,
                "volume": 0,
                "liquidity": "CUSTOM"
            })
            seen.add(symbol)

    # 2️⃣ باقي السوق
    market_symbols = filter_and_merge_markets()

    for m in market_symbols:
        if m["symbol"] in seen:
            continue

        watchlist.append(m)
        seen.add(m["symbol"])

        if len(watchlist) >= limit:
            break

    return watchlist


if __name__ == "__main__":
    wl = get_watchlist()
    print(f"TOTAL MARKETS: {len(wl)}")
    for m in wl[:10]:
        print(m)