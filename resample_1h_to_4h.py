
# resample_1h_to_4h.py

import pandas as pd
import os

in_path = "data/1h/btc_1h_historical.csv"
out_path = "data/4h/btc_4h_historical.csv"

if not os.path.exists(in_path):
    print(f"❌ Source file not found: {in_path}")
    exit()

df = pd.read_csv(in_path, parse_dates=["timestamp"])
df.set_index("timestamp", inplace=True)

df_4h = df.resample("4h").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
}).dropna().reset_index()

os.makedirs("data/4h", exist_ok=True)
df_4h.to_csv(out_path, index=False)
print(f"✅ Resampled 4H data saved to {out_path} ({len(df_4h)} rows)")
