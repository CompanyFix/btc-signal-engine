
# fetch_all_timeframes_tv.py

from tvdatafeed import TvDatafeed, Interval
import os

tv = TvDatafeed(session='dxs5rz7yywv95asiaarv6rrjzkbgtz9q')

# Timeframe to TradingView Interval mapping and target bar count
intervals = {
    "1m": (Interval.in_1_minute, 100000),
    "5m": (Interval.in_5_minute, 50000),
    "15m": (Interval.in_15_minute, 50000),
    "1h": (Interval.in_1_hour, 10000),
    "4h": (Interval.in_4_hour, 10000),
    "8h": (Interval.in_8_hour, 10000),
    "12h": (Interval.in_12_hour, 10000),
    "18h": (Interval.in_18_hour, 10000),
    "1d": (Interval.in_1_day, 10000),
    "3d": (Interval.in_3_day, 5000),
    "5d": (Interval.in_5_day, 5000),
}

symbol = 'BTCUSDT'
exchange = 'BINANCE'

for tf, (interval, n_bars) in intervals.items():
    print(f"📥 Fetching {n_bars} bars for {tf} from TradingView...")
    try:
        df = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=n_bars)
        if df is None or df.empty:
            print(f"⚠️ No data returned for {tf}")
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
