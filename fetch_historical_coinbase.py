
# fetch_historical_coinbase.py

import ccxt
import pandas as pd
import os
import time
from datetime import datetime, timedelta

exchange = ccxt.coinbase()

symbol = "BTC/USD"
start_date = datetime(2021, 1, 1)
end_date = datetime.utcnow()
max_limit = 300  # Coinbase often returns 300 per call

# timeframe: (label, minutes per candle)
timeframes = {
    "1m": ("1m", 1),
    "5m": ("5m", 5),
    "15m": ("15m", 15),
    "1h": ("1h", 60),
    "4h": ("4h", 240),
    "8h": ("1h", 480),
    "12h": ("1h", 720),
    "1d": ("1d", 1440)
}

def fetch_timeframe(tf_key, tf_coinbase, tf_minutes):
    print(f"📥 Fetching {tf_key} data...")
    all_data = []
    since = int(start_date.timestamp() * 1000)
    now_ms = int(end_date.timestamp() * 1000)
    step = tf_minutes * 60 * 1000 * max_limit

    while since < now_ms:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=tf_coinbase, since=since, limit=max_limit)
            if not ohlcv:
                break
            all_data += ohlcv
            since = ohlcv[-1][0] + 1
            time.sleep(exchange.rateLimit / 1000)
        except Exception as e:
            print(f"❌ Error fetching {tf_key}: {e}")
            break

    if not all_data:
        print(f"⚠️ No data returned for {tf_key}")
        return

    df = pd.DataFrame(all_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    out_dir = f"data/{tf_key}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/btc_{tf_key}_historical.csv"
    df.to_csv(out_path, index=False)
    print(f"✅ Saved {len(df)} rows to {out_path}")

if __name__ == "__main__":
    for tf_key, (tf_coinbase, tf_minutes) in timeframes.items():
        fetch_timeframe(tf_key, tf_coinbase, tf_minutes)
