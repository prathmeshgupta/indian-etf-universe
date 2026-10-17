# Indian ETF Universe: AMFI NAVs & Premium/Discount Tracker

Complete registry of **350+ Exchange Traded Funds (ETFs)** listed on the National Stock Exchange of India (NSE), with official daily Net Asset Values (NAV) from the Association of Mutual Funds in India (AMFI) and secondary market premium/discount spread tracking.

Companion repository to [`prathmeshgupta/nifty-pit-universe`](https://github.com/prathmeshgupta/nifty-pit-universe).

---

## 📊 Summary of Datasets

All processed datasets are saved in [`output/`](output/):

| Dataset | Observations | Unique Schemes | Source | Formats |
| :--- | :---: | :---: | :--- | :--- |
| **ETF Tracking & NAVs** | **608** | **608** | AMFI Official Daily Flat File | [`etf_tracking.parquet`](output/etf_tracking.parquet), [`etf_tracking.csv`](output/etf_tracking.csv) |
| **NSE ETF Registry** | **355** | **355** | NSE Exchange Equity Division | [`etf_registry.csv`](output/etf_registry.csv) |

---

## 💡 Why This Exists: The ETF Execution & Arbitrage Gap

In systematic multi-asset strategies (such as Dual Momentum ETF rotations, Gilt allocations, and Gold hedges), backtesting on closing market prices alone causes severe distortions:
1. **Illiquidity & Premium Distortion**: Indian ETFs frequently trade at significant deviations from fair value (often $1\%\text{--}4\%$ premium or discount) due to authorized participant (AP) creation basket bottlenecks.
2. **NAV vs. Price Divergence**: If an algorithm assumes it can enter an ETF at its fair-value closing NAV, but the secondary market was bid up with a $2.5\%$ premium, the real-world strategy suffers instant execution drag.
3. **Asset Class Segmentation**: Indian ETFs span Equity, Target Maturity Debt/Gilt, Commodities (Gold/Silver), and Global/US proxies. Each category behaves differently in tracking efficiency.

This repository tracks both official daily NAV and exchange closing prices to monitor tracking errors and filter out illiquid ETFs before inclusion in strategy universes.

---

## 🧱 Data Schema

### `etf_tracking`
| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `scheme_code` | String | AMFI mutual fund identifier | `151533` |
| `isin` | String | Permanent security ISIN | `INF209KB18T9` |
| `scheme_name` | String | Full registered fund name | `Aditya Birla Sun Life CRISIL Liquid Overnight ETF` |
| `official_nav` | Float | Official AMC Net Asset Value (INR) | `1000.0000` |
| `nav_date` | Date | NAV valuation date | `2026-10-16` |
| `market_close` | Float | Secondary exchange trade close | `1000.15` |
| `premium_discount_pct` | Float | Spread % = `((Close - NAV) / NAV) * 100` | `+0.015%` |

---

## 🔍 How to Query

### 1. Using Python & Pandas
```python
import pandas as pd

df = pd.read_parquet("output/etf_tracking.parquet")

# Inspect all Sovereign Gold & Silver ETFs
precious_metals = df[df["scheme_name"].str.contains("GOLD|SILVER", case=False, na=False)]
print(f"Precious Metal ETFs: {len(precious_metals)}")
print(precious_metals[["isin", "scheme_name", "official_nav"]].head(10))
```

### 2. Using the CLI Helper
```bash
# Query all Gilt & Government Bond ETFs
python runner.py --query GILT
```

---

## 🧪 Quality Audit
```bash
python evaluate_quality.py
```
* **NAV Integrity**: 0 null NAVs, 0 non-positive NAV values ([PASS]).
* **Registry Coverage**: 600+ active ETF share classes indexed ([PASS]).

---

## 📄 License
MIT License. Copyright (c) 2026 Prathmesh Gupta.
