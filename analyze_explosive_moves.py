
# analyze_explosive_moves.py

import pandas as pd
import numpy as np
import json

def analyze_explosive_moves(csv_path="data/4h/btc_4h_multi_tf.csv", move_threshold=2.0, lookahead=30):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    results = []

    indicator_cols = [col for col in df.columns if any(
        key in col.lower() for key in ["rsi", "vwap", "macd", "ema", "sma", "bb", "atr", "mfi", "stoch"]
    )]

    for i in range(len(df) - lookahead):
        start_row = df.iloc[i]
        end_row = df.iloc[i + lookahead]
        pct_move = (end_row["close"] - start_row["close"]) / start_row["close"] * 100

        if abs(pct_move) >= move_threshold:
            move = {
                "start_time": start_row["timestamp"],
                "end_time": end_row["timestamp"],
                "direction": "up" if pct_move > 0 else "down",
                "move_size": round(pct_move, 2),
                "start_indicators": {col: start_row[col] for col in indicator_cols if pd.notna(start_row[col])},
                "end_indicators": {col: end_row[col] for col in indicator_cols if pd.notna(end_row[col])}
            }
            results.append(move)

    with open("memory/fingerprint_samples.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Found {len(results)} explosive moves > {move_threshold}%")
    print("📁 Fingerprint log saved to memory/fingerprint_samples.json")

if __name__ == "__main__":
    analyze_explosive_moves()
