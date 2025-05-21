
# analyze_explosive_moves_multi_tf.py

import pandas as pd
import numpy as np
import json
import os

# Define how many candles per timeframe = 1 day
CANDLES_PER_DAY = {
    "1m": 1440,
    "5m": 288,
    "15m": 96,
    "1h": 24,
    "4h": 6,
    "8h": 3,
    "12h": 2,
    "1d": 1
}

def analyze_moves_for_tf(tf, path, move_threshold=2.0):
    lookahead = CANDLES_PER_DAY[tf]
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    indicator_cols = [col for col in df.columns if any(
        key in col.lower() for key in ["rsi", "vwap", "macd", "ema", "sma", "bb", "atr", "mfi", "stoch"]
    )]

    results = []
    for i in range(len(df) - lookahead):
        start_row = df.iloc[i]
        end_row = df.iloc[i + lookahead]
        pct_move = (end_row["close"] - start_row["close"]) / start_row["close"] * 100

        if abs(pct_move) >= move_threshold:
            results.append({
                "timeframe": tf,
                "start_time": start_row["timestamp"],
                "end_time": end_row["timestamp"],
                "direction": "up" if pct_move > 0 else "down",
                "move_size": round(pct_move, 2),
                "start_indicators": {col: start_row[col] for col in indicator_cols if pd.notna(start_row[col])},
                "end_indicators": {col: end_row[col] for col in indicator_cols if pd.notna(end_row[col])}
            })

    return results

def run_all():
    all_moves = []
    base_dir = "data"

    for tf in CANDLES_PER_DAY:
        file_path = f"{base_dir}/{tf}/btc_{tf}_indicators.csv"
        if not os.path.exists(file_path):
            print(f"⚠️ Skipping {tf} — file not found.")
            continue

        print(f"🔍 Scanning {tf} timeframe...")
        tf_moves = analyze_moves_for_tf(tf, file_path)
        all_moves.extend(tf_moves)

    out_path = "memory/fingerprint_samples_multi_tf.json"
    with open(out_path, "w") as f:
        json.dump(all_moves, f, indent=2)

    print(f"✅ Found {len(all_moves)} multi-timeframe explosive moves")
    print(f"📁 Saved to {out_path}")

if __name__ == "__main__":
    run_all()
