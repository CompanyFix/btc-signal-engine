
# analyze_drawdown_signal_candidates.py

import pandas as pd
import json

def analyze_drawdown_signals(log_path="memory/rule_backtest_log.csv"):
    df = pd.read_csv(log_path)

    df["rsi_at_drawdown"] = df["rsi_at_drawdown"].apply(json.loads)

    rsi_columns = set()
    for r in df["rsi_at_drawdown"]:
        rsi_columns.update(r.keys())
    rsi_columns = sorted(list(rsi_columns))

    win_rows = df[df["true_win"] == True]
    loss_rows = df[df["true_win"] == False]

    def summarize_rsi_distribution(rows, label):
        stats = []
        for col in rsi_columns:
            values = [float(r.get(col)) for r in rows["rsi_at_drawdown"] if col in r and pd.notna(r[col])]
            if values:
                stats.append({
                    "RSI_Column": col,
                    "Label": label,
                    "Count": len(values),
                    "Avg": round(sum(values) / len(values), 2),
                    "Min": round(min(values), 2),
                    "Max": round(max(values), 2)
                })
        return stats

    win_summary = summarize_rsi_distribution(win_rows, "WIN")
    loss_summary = summarize_rsi_distribution(loss_rows, "LOSS")

    df_summary = pd.DataFrame(win_summary + loss_summary)
    df_summary.to_csv("memory/drawdown_rsi_signal_training.csv", index=False)
    print("✅ RSI drawdown signal summary saved to memory/drawdown_rsi_signal_training.csv")
    print(df_summary)

if __name__ == "__main__":
    analyze_drawdown_signals()
