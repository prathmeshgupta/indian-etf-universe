import argparse
import pandas as pd
from pathlib import Path
from indian_etf_universe.fetcher import IndianETFFetcher

def main():
    parser = argparse.ArgumentParser(description="Indian ETF Universe & NAV Tracker")
    parser.add_argument("--query", help="Filter ETFs by name keyword (e.g. NIFTY, GILT, GOLD, BHARAT)")
    parser.add_argument("--sync", action="store_true", help="Sync latest daily NAVs from AMFI")
    args = parser.parse_args()

    csv_path = Path(__file__).parent / "output" / "etf_tracking.csv"
    if not csv_path.exists():
        print("Output file not found. Run sync first.")
        return

    df = pd.read_csv(csv_path)
    if args.query:
        matches = df[df["scheme_name"].str.contains(args.query, case=False, na=False)]
        print(f"\n--- ETFs matching '{args.query}' (Count: {len(matches)}) ---")
        print(matches[["isin", "scheme_name", "official_nav"]].head(25).to_string())
    elif args.sync:
        fetcher = IndianETFFetcher()
        live = fetcher.fetch_amfi_etf_navs()
        print(f"Retrieved {len(live)} ETF NAVs from AMFI.")
    else:
        print(f"Loaded {len(df)} ETF NAV records. Use --query <KEYWORD> or --sync.")

if __name__ == "__main__":
    main()
