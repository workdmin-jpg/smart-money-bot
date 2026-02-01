def strong_close(candle):
    open_price = candle[0]
    high = candle[1]
    low = candle[2]
    close = candle[3]

    body = abs(close - open_price)
    range_ = high - low

    if range_ == 0:
        return False

    return (body / range_) >= 0.6