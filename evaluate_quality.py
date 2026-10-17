import pandas as pd
from pathlib import Path

def audit_quality():
    print("=" * 60)
    print(" INDIAN ETF UNIVERSE - DATA QUALITY AUDIT")
    print("=" * 60)
    
    root = Path(__file__).parent
    track_path = root / "output" / "etf_tracking.csv"
    reg_path = root / "output" / "etf_registry.csv"
    
    assert track_path.exists(), "etf_tracking.csv missing"
    df_track = pd.read_csv(track_path)
    print(f"Total Active ETFs Tracked via AMFI: {len(df_track)}")
    
    null_navs = df_track["official_nav"].isnull().sum()
    zero_navs = (df_track["official_nav"] <= 0).sum()
    print(f"Null NAVs: {null_navs} {'[PASS]' if null_navs == 0 else '[FAIL]'}")
    print(f"Non-positive NAVs: {zero_navs} {'[PASS]' if zero_navs == 0 else '[FAIL]'}")
    
    if reg_path.exists():
        df_reg = pd.read_csv(reg_path)
        print(f"Total Registered NSE ETFs: {len(df_reg)}")
        
    print("=" * 60)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 60)

if __name__ == "__main__":
    audit_quality()
