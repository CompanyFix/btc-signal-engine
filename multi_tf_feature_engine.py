
# multi_tf_feature_engine.py

import pandas as pd
import os

BASE_TF = "4h"
base_file = f"data/{BASE_TF}/btc_{BASE_TF}_indicators.csv"

# Only timeframes we can safely use for now
all_timeframes = [
    "1m", "5m", "15m", "1h", "8h", "12h"
]

print(f"📊 Loading base timeframe: {BASE_TF}")
df_base = pd.read_csv(base_file)
df_base["timestamp"] = pd.to_datetime(df_base["timestamp"])
df_base = df_base.sort_values("timestamp")

critical_cols = ["rsi", "ema_20", "macd"]
before_merge_len = len(df_base)
missing_timeframes = []
skipped_due_to_row_loss = []

for tf in all_timeframes:
    tf_file = f"data/{tf}/btc_{tf}_indicators.csv"
    if not os.path.exists(tf_file):
        print(f"❌ Skipping {tf} — file not found.")
        missing_timeframes.append(tf)
        continue

    df_other = pd.read_csv(tf_file)
    df_other["timestamp"] = pd.to_datetime(df_other["timestamp"])
    df_other = df_other.set_index("timestamp").resample("4h").last().reset_index()

    suffix = f"_{tf}"
    df_other = df_other.add_suffix(suffix)
    df_other = df_other.rename(columns={f"timestamp{suffix}": "timestamp"})

    temp_merged = df_base.merge(df_other, on="timestamp", how="left")
    after_merge_len = temp_merged.dropna(subset=critical_cols).shape[0]
    row_loss_pct = 100 * (1 - after_merge_len / before_merge_len) if before_merge_len else 0

    if row_loss_pct >= 90:
        print(f"⚠️ Skipping {tf} — caused {row_loss_pct:.1f}% row loss after merge.")
        skipped_due_to_row_loss.append(tf)
        continue

    print(f"🔗 Merging {tf} into base timeframe... ({after_merge_len} rows remaining)")
    df_base = temp_merged

# Drop rows only if critical base indicators are missing
df_base = df_base.dropna(subset=critical_cols)
df_base = df_base.ffill()

output_file = f"data/{BASE_TF}/btc_{BASE_TF}_multi_tf.csv"
df_base.to_csv(output_file, index=False)

print(f"✅ Multi-timeframe dataset saved to: {output_file}")
print(f"📈 Final rows: {len(df_base)} | Final columns: {df_base.shape[1]}")

if missing_timeframes:
    print(f"⚠️ Missing timeframes: {', '.join(missing_timeframes)}")
if skipped_due_to_row_loss:
    print(f"⚠️ Skipped due to row loss: {', '.join(skipped_due_to_row_loss)}")
