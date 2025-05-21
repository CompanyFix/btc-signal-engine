
import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class Interval:
    in_1_minute = "1m"
    in_5_minute = "5m"
    in_15_minute = "15m"
    in_1_hour = "1h"
    in_4_hour = "4h"
    in_8_hour = "8h"
    in_12_hour = "12h"
    in_1_day = "1d"
    in_3_day = "3d"
    in_5_day = "5d"

class TvDatafeed:
    def __init__(self, session=None, auth_token=None):
        self.session = requests.Session()
        if session:
            self.session.cookies.set("session", session)
        if auth_token:
            self.session.cookies.set("auth_token", auth_token)

    def get_hist(self, symbol, exchange, interval, n_bars=5000):
        # Simulate realistic candle data for testing only (replace this with true scraping if needed)
        print(f"🔧 [Simulated fetch] Getting {n_bars} bars for {symbol} ({interval}) from {exchange}")
        now = pd.Timestamp.utcnow().floor('1min')
        interval_map = {
            "1m": "1min",
            "5m": "5min",
            "15m": "15min",
            "1h": "1h",
            "4h": "4h",
            "8h": "8h",
            "12h": "12h",
            "1d": "1d",
            "3d": "3d",
            "5d": "5d"
        }

        freq = interval_map.get(interval, "1h")
        dates = pd.date_range(end=now, periods=n_bars, freq=freq)
        prices = np.cumsum(np.random.normal(0, 1, size=n_bars)) + 30000

        df = pd.DataFrame({
            "datetime": dates,
            "open": prices,
            "high": prices + np.random.rand(n_bars) * 20,
            "low": prices - np.random.rand(n_bars) * 20,
            "close": prices + np.random.randn(n_bars),
            "volume": np.random.randint(100, 1000, size=n_bars)
        })
        return df
