
# real_time_rsi_alerts.py

import pandas as pd
import numpy as np

RSI_WIN_AVG = 39.8  # From drawdown signal training
RSI_WIN_RANGE = 5.0  # Acceptable variance for match
CONFIDENCE_THRESHOLD = 0.5  # Optional: minimum win rate confidence

def latest_rsi_signal(csv_path="data/4h/btc_4h_multi_tf.csv"):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp")

    rsi_cols = [col for col in df.columns if "rsi" in col.lower()]
    latest = df.iloc[-1]
    current_rsis = {col: latest[col] for col in rsi_cols if pd.notna(latest[col])}

    print(f"🕒 Analyzing latest RSI values at: {latest['timestamp']}")
    for col, val in current_rsis.items():
        print(f"{col}: {val:.2f}")

    rsi_avg = np.mean(list(current_rsis.values()))
    print(f"📊 RSI Avg: {rsi_avg:.2f} | Win Profile Avg: {RSI_WIN_AVG}")

    if abs(rsi_avg - RSI_WIN_AVG) <= RSI_WIN_RANGE:
        print("📢 ALERT: RSI profile matches historical WIN condition")
        print("⚡ Suggested Action: SHORT (RSI aligns with past winning drawdown signals)")
    else:
        print("✅ No match to winning profile at this time.")

if __name__ == "__main__":
    latest_rsi_signal()
