
import pandas as pd
import os
import json

LOOKAHEAD = 30

def evaluate_trade(signal_row, df, direction):
    entry_price = signal_row['close']
    entry_index = signal_row.name
    future_data = df.iloc[entry_index+1 : entry_index+1+LOOKAHEAD]

    if future_data.empty:
        return None

    prices = future_data['close']
    lows = future_data['low']
    min_price = lows.min()
    final_price = prices.iloc[-1]
    max_price = prices.max()

    # Find row of max drawdown
    drawdown_row = future_data.loc[lows.idxmin()]
    drawdown_rsi_values = {col: drawdown_row[col] for col in drawdown_row.index if "rsi" in col.lower()}

    result = {
        "timestamp": signal_row["timestamp"],
        "entry_price": entry_price,
        "final_price": final_price,
        "max_run_up": (max_price - entry_price) / entry_price * 100,
        "max_drawdown": (min_price - entry_price) / entry_price * 100,
        "net_pct_change": (final_price - entry_price) / entry_price * 100,
        "direction": direction,
        "rule_name": signal_row.get("rule_name", "N/A"),
        "rsi_at_max_drawdown": drawdown_rsi_values
    }

    result["true_win"] = result["net_pct_change"] > 0 if direction == "long" else result["net_pct_change"] < 0
    return result

def ask_confidence(csv_path, query_time, direction, allow_missing=False):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    query_time = pd.to_datetime(query_time)

    if query_time.tzinfo is None:
        query_time = query_time.tz_localize("UTC")
    else:
        query_time = query_time.tz_convert("UTC")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    df_past = df[df["timestamp"] < query_time].copy()
    if df_past.empty:
        print("❌ No historical data found before the query time.")
        return

    target_row = df_past.iloc[-1]
    target_index = df_past.index[-1]

    rsi_cols = [col for col in df.columns if "rsi" in col.lower()]
    rsi_values = {col: target_row[col] for col in rsi_cols}

    missing_rsi = [col for col, val in rsi_values.items() if pd.isna(val)]
    valid_rsi = {col: val for col, val in rsi_values.items() if pd.notna(val)}

    print("🕵️ RSI Values at query time:")
    for col in rsi_cols:
        val = rsi_values[col]
        status = "✅" if pd.notna(val) else "❌ MISSING"
        print(f"{col}: {val:.2f}" if pd.notna(val) else f"{col}: {status}")

    if not allow_missing and missing_rsi:
        print("📉 Rule not triggered — missing RSI values.")
        return

    if direction == "long" and all(val >= 50.01 for val in valid_rsi.values()):
        triggered_rule = "rsi_all_bullish"
    elif direction == "short" and all(val <= 50.00 for val in valid_rsi.values()):
        triggered_rule = "rsi_all_bearish"
    else:
        print(f"📉 Rule not triggered — not all RSI values meet {direction.upper()} criteria.")
        return

    result = evaluate_trade(df.loc[target_index], df, direction)
    if not result:
        print("❌ Not enough future data to evaluate trade outcome.")
        return

    # Historical rule confidence
    historical_results = []
    for i, row in df_past.iterrows():
        row_rsis = [row[col] for col in rsi_cols if pd.notna(row[col])]
        if direction == "long" and all(val >= 50.01 for val in row_rsis):
            match = True
        elif direction == "short" and all(val <= 50.00 for val in row_rsis):
            match = True
        else:
            continue

        if match:
            r_result = evaluate_trade(row, df, direction)
            if r_result:
                historical_results.append(r_result["true_win"])

    confidence = sum(historical_results) / len(historical_results) if historical_results else 0

    print(f"🕒 Query Time: {query_time}")
    print(f"🔍 Rule Triggered: {triggered_rule}")
    print(f"📊 Predicted Confidence: {confidence*100:.2f}%")
    print(f"📉 Max Drawdown: {result['max_drawdown']:.2f}%")
    print(f"📈 Max Run-up: {result['max_run_up']:.2f}%")
    print(f"💰 Net Gain/Loss: {result['net_pct_change']:.2f}%")
    print(f"✅ Outcome: {'Win' if result['true_win'] else 'Loss'}")

    log_df = pd.DataFrame([{
        "timestamp": query_time,
        "direction": direction,
        "rule": triggered_rule,
        "confidence": confidence,
        "drawdown": result["max_drawdown"],
        "run_up": result["max_run_up"],
        "net_change": result["net_pct_change"],
        "true_win": result["true_win"],
        "rsi_at_max_drawdown": json.dumps(result["rsi_at_max_drawdown"])
    }])

    os.makedirs("memory", exist_ok=True)
    logfile = "memory/strategy_results_log.csv"
    if os.path.exists(logfile):
        log_df.to_csv(logfile, mode="a", header=False, index=False)
    else:
        log_df.to_csv(logfile, index=False)
