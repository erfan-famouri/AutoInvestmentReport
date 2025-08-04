import pandas as pd
import json
from datetime import datetime
import os

def main(
    prices_csv: str = "prices_history.csv",
    assets_json: str = "user_assets.json",
    output_json: str = "portfolio_summary.json"
):
    # 1) Load user assets
    with open(assets_json, 'r', encoding='utf-8') as f:
        assets: dict[str, float] = json.load(f)
    
    # 2) Load price history (long format) and clean numeric columns
    df = pd.read_csv(prices_csv)
    # Ensure sell_price is float (remove commas if present)
    df['sell_price'] = (
        df['sell_price']
        .astype(str)
        .str.replace(',', '', regex=False)
        .astype(float)
    )
    # Parse dates
    df['date'] = pd.to_datetime(df['date'])
    
    # 3) Find the timestamp of the latest prices
    latest_time = df['date'].max()
    latest_df = df[df['date'] == latest_time]
    
    # 4) Build a dict: subject → latest sell_price
    latest_prices = dict(zip(latest_df['subject'], latest_df['sell_price']))
    
    # 5) Compute assets_rial (skip cash "ریال")
    assets_rial = 0.0
    for asset_name, amount in assets.items():
        if asset_name == "ریال":
            continue
        if asset_name not in latest_prices:
            raise KeyError(f"No price for '{asset_name}' at {latest_time}")
        assets_rial += amount * latest_prices[asset_name]
    
    # 6) Extract cash in Toman
    cash_toman = assets.get("ریال", 0)
    
    # 7) Compute total_toman (assets + cash)
    total_toman = int(assets_rial + cash_toman)
    
    # 8) Convert that full total to USD with +10 000 adjustment
    dollar_price = latest_prices.get("دلار آمریکا")
    if dollar_price is None:
        raise KeyError(f"No 'دلار آمریکا' price at {latest_time}")
    total_dollar = round(total_toman / (dollar_price + 10_000), 2)
    
    # 9) Build the new summary record
    summary = {
        "datetime": latest_time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_toman": total_toman,
        "total_dollar": total_dollar,
        "cash_toman": cash_toman
    }
    
    # 10) Load existing portfolio_summary.json (or start fresh)
    data = []
    if os.path.exists(output_json) and os.path.getsize(output_json) > 0:
        with open(output_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    # 11) Append new record and save
    data.append(summary)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 12) Print feedback
    print(f"[{summary['datetime']}] New record added:")
    print(f"  • total_toman   = {summary['total_toman']:,} toman (incl. cash)")
    print(f"  • total_dollar  = {summary['total_dollar']:,} USD")
    print(f"  • cash_toman    = {summary['cash_toman']:,} toman")
    
    return summary

if __name__ == "__main__":
    main()
