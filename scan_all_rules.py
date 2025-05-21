
# scan_all_rules.py

import pandas as pd
from strategy_engine import evaluate_trade
import json

def scan_rsi_strategy(csv_path, direction="short", lookahead=30, save_path="memory/rule_backtest_log.csv"):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    rsi_cols = [col for col in df.columns if "rsi" in col.lower()]
    results = []

    for i in range(len(df) - lookahead):
        row = df.iloc[i]
        row_rsis = {col: row[col] for col in rsi_cols if pd.notnull(row[col])}
        if not row_rsis:
            continue

        if direction == "long" and all(val >= 50.01 for val in row_rsis.values()):
            rule = "rsi_all_bullish"
        elif direction == "short" and all(val <= 50.00 for val in row_rsis.values()):
            rule = "rsi_all_bearish"
        else:
            continue

        result = evaluate_trade(row, df, direction)
        if result:
            results.append({
                "timestamp": row["timestamp"],
                "rule": rule,
                "direction": direction,
                "net_pct_change": result["net_pct_change"],
                "drawdown": result["max_drawdown"],
                "run_up": result["max_run_up"],
                "true_win": result["true_win"],
                "rsi_at_drawdown": json.dumps(result["rsi_at_max_drawdown"])
            })

    results_df = pd.DataFrame(results)
    if not results_df.empty:
        results_df.to_csv(save_path, index=False)
        print(f"✅ Scanned {len(results_df)} signals and saved to: {save_path}")
        print(results_df.head(10))
    else:
        print("❌ No valid signals found with current criteria.")

if __name__ == "__main__":
    scan_rsi_strategy("data/4h/btc_4h_multi_tf.csv", direction="short")
