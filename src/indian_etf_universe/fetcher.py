import io
import requests
import pandas as pd
from typing import Optional

AMFI_NAV_ALL_URL = "https://www.amfiindia.com/spages/NAVAll.txt"
NSE_ETF_REGISTRY_URL = "https://archives.nseindia.com/content/equities/eq_etfseclist.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

class IndianETFFetcher:
    """Fetches official Indian ETF Net Asset Values (AMFI) and NSE ETF Registry."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_amfi_etf_navs(self) -> pd.DataFrame:
        resp = self.session.get(AMFI_NAV_ALL_URL, timeout=30)
        resp.raise_for_status()
        lines = resp.text.splitlines()

        records = []
        for line in lines:
            parts = [p.strip() for p in line.split(";")]
            if len(parts) >= 8:
                scheme_code = parts[0]
                isin_growth = parts[1]
                isin_reinvest = parts[2]
                scheme_name = parts[3]
                nav_str = parts[6]
                nav_date_raw = parts[7]
                try:
                    nav_date = pd.to_datetime(nav_date_raw).strftime("%Y-%m-%d")
                except:
                    nav_date = nav_date_raw

                if "ETF" in scheme_name.upper() or "EXCHANGE TRADED" in scheme_name.upper():
                    try:
                        nav_val = float(nav_str)
                        isin = isin_growth if (isin_growth and isin_growth != "-") else isin_reinvest
                        if isin == "-":
                            isin = None

                        records.append({
                            "scheme_code": scheme_code,
                            "isin": isin,
                            "scheme_name": scheme_name,
                            "official_nav": nav_val,
                            "nav_date": nav_date,
                            "source": "AMFI_OFFICIAL"
                        })
                    except ValueError:
                        continue
        return pd.DataFrame(records)

    def fetch_nse_etf_registry(self) -> pd.DataFrame:
        resp = self.session.get(NSE_ETF_REGISTRY_URL, timeout=15)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text))
        df.columns = [c.strip().replace(" ", "_").upper() for c in df.columns]
        rename_map = {
            "SECURITY_NAME": "security_name",
            "SYMBOL": "symbol",
            "UNDERLYING": "underlying",
            "ISIN_CODE": "isin",
            "ISIN": "isin"
        }
        return df.rename(columns=rename_map)
