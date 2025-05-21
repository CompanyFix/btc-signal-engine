
# optimize_rsi_per_timeframe.py

import pandas as pd
from strategy_engine import evaluate_trade

def test_rsi_column(df, col, direction="short", lookahead=30, rsi_min=45, rsi_max=55, step=0.5):
    results = []
    thresholds = [round(rsi_min + step * i, 2) for i in range(int((rsi_max - rsi_min) / step) + 1)]

    for threshold in thresholds:
        trades = 0
        wins = 0
        net_changes = []

        for i in range(len(df) - lookahead):
            row = df.iloc[i]
            rsi_value = row.get(col, None)

            if pd.isna(rsi_value):
                continue

            if direction == "long" and rsi_value >= threshold:
                valid = True
            elif direction == "short" and rsi_value <= threshold:
                valid = True
            else:
                continue

            trades += 1
            result = evaluate_trade(row, df, direction)
            if result:
                wins += int(result["true_win"])
                net_changes.append(result["net_pct_change"])

        if trades > 0:
            win_rate = wins / trades
            avg_gain = sum(net_changes) / len(net_changes)
            results.append({
                "rsi_column": col,
                "threshold": threshold,
                "direction": direction,
                "trades": trades,
                "win_rate": round(win_rate * 100, 2),
                "avg_gain": round(avg_gain, 5)
            })

    return results

def optimize_rsi_per_column(csv_path, direction="short"):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    rsi_cols = [col for col in df.columns if "rsi" in col.lower()]
    all_results = []

    for col in rsi_cols:
        print(f"🔍 Testing {col}...")
        res = test_rsi_column(df, col, direction=direction)
        all_results.extend(res)

    df_results = pd.DataFrame(all_results)
    df_results = df_results.sort_values("win_rate", ascending=False)
    df_results.to_csv("memory/rsi_column_optimization_log.csv", index=False)
    print(df_results.head(10))
    print("✅ RSI column-level optimization complete.")
    print("📁 Saved to: memory/rsi_column_optimization_log.csv")

if __name__ == "__main__":
    optimize_rsi_per_column("data/4h/btc_4h_multi_tf.csv", direction="short")
