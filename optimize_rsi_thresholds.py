
# optimize_rsi_thresholds.py

import pandas as pd
from strategy_engine import evaluate_trade

def scan_rsi_with_thresholds(csv_path, rsi_min=45, rsi_max=55, step=0.5, direction="long", lookahead=30):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    rsi_cols = [col for col in df.columns if "rsi" in col.lower()]
    results = []

    thresholds = [round(rsi_min + step * i, 2) for i in range(int((rsi_max - rsi_min) / step) + 1)]

    for threshold in thresholds:
        match_count = 0
        wins = 0
        net_changes = []

        for i in range(len(df) - lookahead):
            row = df.iloc[i]
            rsis = [row[col] for col in rsi_cols if pd.notna(row[col])]

            if not rsis:
                continue

            if direction == "long" and all(val >= threshold for val in rsis):
                rule = f"RSI_all_≥_{threshold}"
            elif direction == "short" and all(val <= threshold for val in rsis):
                rule = f"RSI_all_≤_{threshold}"
            else:
                continue

            match_count += 1
            result = evaluate_trade(row, df, direction)
            if result:
                wins += int(result["true_win"])
                net_changes.append(result["net_pct_change"])

        if match_count:
            win_rate = wins / match_count
            avg_gain = sum(net_changes) / len(net_changes) if net_changes else 0
            results.append({
                "threshold": threshold,
                "rule": rule,
                "direction": direction,
                "trades": match_count,
                "win_rate": round(win_rate * 100, 2),
                "avg_gain": round(avg_gain, 5)
            })

    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values("win_rate", ascending=False)
    df_results.to_csv("memory/rsi_threshold_optimization_log.csv", index=False)
    print(df_results.head(10))
    print("✅ Optimization complete. Results saved to memory/rsi_threshold_optimization_log.csv")

if __name__ == "__main__":
    scan_rsi_with_thresholds(
        csv_path="data/4h/btc_4h_multi_tf.csv",
        rsi_min=45,
        rsi_max=55,
        step=0.5,
        direction="short"
    )
