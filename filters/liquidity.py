# filters/liquidity.py

def classify_liquidity(volume_usdt):
    """
    تصنيف السيولة حسب حجم التداول اليومي (USDT)
    """
    if volume_usdt >= 50_000_000:
        return "HIGH"      # مؤسسات / آمن
    elif volume_usdt >= 5_000_000:
        return "MEDIUM"    # متوسط / حذر
    elif volume_usdt >= 500_000:
        return "LOW"       # ضعيف / خطر
    else:
        return "DEAD"      # ممنوع التداول