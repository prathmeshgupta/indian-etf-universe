"""
Automated Weekly Dataset Updater for indian-etf-universe
Can be executed locally or via GitHub Actions.
Zero credentials required.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from indian_etf_universe.fetcher import IndianETFFetcher

OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TRACK_CSV = OUTPUT_DIR / "etf_tracking.csv"
TRACK_PARQUET = OUTPUT_DIR / "etf_tracking.parquet"
REG_CSV = OUTPUT_DIR / "etf_registry.csv"


def update():
    print("[1/3] Fetching latest official AMFI NAVs and NSE ETF Registry...")
    fetcher = IndianETFFetcher()
    
    nav_df = fetcher.fetch_amfi_etf_navs()
    reg_df = fetcher.fetch_nse_etf_registry()
    print(f"      Retrieved {len(nav_df)} active ETF NAVs and {len(reg_df)} registered ETFs.")

    print("[2/3] Updating output datasets...")
    if not nav_df.empty:
        nav_df = nav_df.dropna(subset=["isin", "official_nav"])
        nav_df = nav_df.drop_duplicates(subset=["isin", "nav_date"], keep="last")
        nav_df = nav_df.sort_values(by=["nav_date", "scheme_name"], ascending=[False, True])

        nav_df.to_csv(TRACK_CSV, index=False)
        nav_df.to_parquet(TRACK_PARQUET, index=False)
        print(f"      Saved {len(nav_df)} ETF NAVs to {TRACK_CSV.name} and {TRACK_PARQUET.name}.")

    if not reg_df.empty:
        reg_df.to_csv(REG_CSV, index=False)
        print(f"      Saved {len(reg_df)} registered ETFs to {REG_CSV.name}.")

    print("[3/3] Running automated quality audit...")
    from evaluate_quality import audit_quality
    audit_quality()
    print("Update complete successfully.")


if __name__ == "__main__":
    update()
