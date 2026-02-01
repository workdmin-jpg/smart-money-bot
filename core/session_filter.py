from datetime import datetime, timezone

def is_trading_session():
    now = datetime.now(timezone.utc)
    hour = now.hour

    # London session
    if 8 <= hour <= 11:
        return True

    # New York session
    if 13 <= hour <= 16:
        return True

    return False