
# fetch_real_data_ccxt.py

import ccxt
import pandas as pd
import os
import time

exchange = ccxt.binance()

# Mapping of internal timeframe labels to Binance timeframes
timeframes = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "4h": "4h",
    "8h": "8h",
    "12h": "12h"
}

symbol = "BTC/USDT"
limit = 1000  # Binance max per call; will paginate

def fetch_ohlcv(tf_key, tf_binance, max_candles=10000):
    print(f"📥 Fetching {tf_key} from Binance...")
    all_data = []
    since = None

    while len(all_data) < max_candles:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=tf_binance, since=since, limit=limit)
            if not ohlcv:
                break
            all_data += ohlcv
            since = ohlcv[-1][0] + 1  # start from just after last timestamp
            time.sleep(exchange.rateLimit / 1000)
        except Exception as e:
            print(f"❌ Error fetching {tf_key}: {e}")
            break

    df = pd.DataFrame(all_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

for tf_key, tf_binance in timeframes.items():
    df = fetch_ohlcv(tf_key, tf_binance, max_candles=10000)
    if df.empty:
        print(f"⚠️ No data for {tf_key}")
        continue
    outdir = f"data/{tf_key}"
    os.makedirs(outdir, exist_ok=True)
    outfile = f"{outdir}/btc_{tf_key}_historical.csv"
    df.to_csv(outfile, index=False)
    print(f"✅ Saved {len(df)} rows to {outfile}")
