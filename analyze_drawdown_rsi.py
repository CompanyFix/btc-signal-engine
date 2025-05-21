
# analyze_drawdown_rsi.py

import pandas as pd
import json
from collections import defaultdict

def analyze_drawdown_rsi(csv_path="memory/rule_backtest_log.csv", drawdown_threshold=-5.0):
    df = pd.read_csv(csv_path)
    rsi_stats = defaultdict(list)

    for _, row in df.iterrows():
        if row["drawdown"] <= drawdown_threshold:
            rsi_data = json.loads(row["rsi_at_drawdown"])
            for rsi_name, value in rsi_data.items():
                if pd.notna(value):
                    rsi_stats[rsi_name].append(value)

    if not rsi_stats:
        print("❌ No qualifying trades found with drawdown below threshold.")
        return

    print(f"📉 RSI values at max drawdown (drawdown ≤ {drawdown_threshold}%):\n")
    summary = []
    for rsi_name, values in rsi_stats.items():
        summary.append({
            "RSI": rsi_name,
            "Count": len(values),
            "Avg RSI": round(sum(values) / len(values), 2),
            "Min": round(min(values), 2),
            "Max": round(max(values), 2)
        })

    df_summary = pd.DataFrame(summary).sort_values("Count", ascending=False)
    print(df_summary.to_string(index=False))
    df_summary.to_csv("memory/rsi_drawdown_summary.csv", index=False)
    print("\n✅ Summary saved to memory/rsi_drawdown_summary.csv")

if __name__ == "__main__":
    analyze_drawdown_rsi()
