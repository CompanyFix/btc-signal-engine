
# fetch_real_data_coinbase.py

import ccxt
import pandas as pd
import os
import time

exchange = ccxt.coinbase()

# Timeframes Coinbase supports through CCXT
timeframes = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "4h": "4h",
    "8h": "1h",     # will manually resample later
    "12h": "1h",    # will manually resample later
}

symbol = "BTC/USD"
limit = 300  # Coinbase's API often returns 300 candles max; we will loop

def fetch_ohlcv(tf_key, tf_ccxt, max_candles=3000):
    print(f"📥 Fetching {tf_key} from Coinbase...")
    all_data = []
    since = None

    while len(all_data) < max_candles:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=tf_ccxt, since=since, limit=limit)
            if not ohlcv:
                break
            all_data += ohlcv
            since = ohlcv[-1][0] + 1
            time.sleep(exchange.rateLimit / 1000)
        except Exception as e:
            print(f"❌ Error fetching {tf_key}: {e}")
            break

    df = pd.DataFrame(all_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Resample if needed
    if tf_key in ["8h", "12h"]:
        df.set_index("timestamp", inplace=True)
        df = df.resample(tf_key).agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        }).dropna().reset_index()

    return df

for tf_key, tf_ccxt in timeframes.items():
    df = fetch_ohlcv(tf_key, tf_ccxt, max_candles=3000)
    if df.empty:
        print(f"⚠️ No data for {tf_key}")
        continue
    outdir = f"data/{tf_key}"
    os.makedirs(outdir, exist_ok=True)
    outfile = f"{outdir}/btc_{tf_key}_historical.csv"
    df.to_csv(outfile, index=False)
    print(f"✅ Saved {len(df)} rows to {outfile}")
