import pandas as pd
from typing import Optional

class ETFSpreadAnalyzer:
    """Calculates premium/discount spreads between secondary exchange price and official NAV."""

    @staticmethod
    def calculate_spread(market_close: float, official_nav: float) -> Optional[float]:
        if official_nav <= 0:
            return None
        return ((market_close - official_nav) / official_nav) * 100.0

    @staticmethod
    def classify_liquidity(premium_discount_pct: float, threshold_pct: float = 2.0) -> str:
        """Flags whether ETF traded within fair-value arbitrage band."""
        if abs(premium_discount_pct) <= threshold_pct:
            return "FAIR_VALUE"
        elif premium_discount_pct > threshold_pct:
            return "SUBSTANTIAL_PREMIUM"
        else:
            return "SUBSTANTIAL_DISCOUNT"
