
# fetch_tradingview_data.py

from tvdatafeed import TvDatafeed, Interval
import os
import pandas as pd

# Use working session-enabled or simulated TvDatafeed
tv = TvDatafeed()

intervals = {
    "1m": Interval.in_1_minute,
    "5m": Interval.in_5_minute,
    "15m": Interval.in_15_minute,
    "1h": Interval.in_1_hour,
    "4h": Interval.in_4_hour,
    "8h": Interval.in_8_hour,
    "12h": Interval.in_12_hour,
    "1d": Interval.in_1_day,
    "3d": Interval.in_3_day,
    "5d": Interval.in_5_day
}

symbol = "BTCUSDT"
exchange = "BINANCE"

for tf, interval in intervals.items():
    try:
        print(f"📥 Fetching {tf} from TradingView...")
        df = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=5000)
        if df is None or df.empty:
            print(f"⚠️ No data for {tf}")
            continue

        df = df.reset_index()
        df = df.rename(columns={
            "datetime": "timestamp",
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
            "volume": "volume"
        })[["timestamp", "open", "high", "low", "close", "volume"]]

        outdir = f"data/{tf}"
        os.makedirs(outdir, exist_ok=True)
        outfile = f"{outdir}/btc_{tf}_historical.csv"
        df.to_csv(outfile, index=False)
        print(f"✅ Saved to {outfile}")
    except Exception as e:
        print(f"❌ Error fetching {tf}: {e}")
