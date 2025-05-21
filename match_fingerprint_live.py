
# match_fingerprint_live.py

import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

def load_live_signature(csv_path="data/4h/btc_4h_multi_tf.csv"):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    latest = df.iloc[-1]
    indicators = {col: latest[col] for col in df.columns if any(
        key in col.lower() for key in ["rsi", "vwap", "macd", "ema", "sma", "bb", "atr", "mfi", "stoch"]
    ) and pd.notna(latest[col])}
    return indicators, latest["timestamp"]

def compare_to_fingerprint(live, fingerprint, tier):
    keys = list(set(live.keys()) & set(fingerprint.keys()))
    print(f"🧠 Using {len(keys)} shared indicators for tier: {tier}")
    if len(keys) < 5:
        print("⚠️ Not enough shared indicators to compute meaningful match.")
        return 0.0

    print("   -", keys)
    live_vec = [live[k] for k in keys]
    ref_vec = [fingerprint[k] for k in keys]

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform([live_vec, ref_vec])
    score = cosine_similarity([scaled[0]], [scaled[1]])[0][0]
    return round(score * 100, 2)

def match_fingerprint_live():
    with open("memory/fingerprint_clusters.json", "r") as f:
        clusters = json.load(f)

    live, timestamp = load_live_signature()
    print(f"🕒 Latest Timestamp: {timestamp}")
    match_scores = {}
    passed = True

    tiers = ["2-3%", "3-5%", "5-10%", "10%+"]
    for i, tier in enumerate(tiers):
        if tier not in clusters or "avg_start" not in clusters[tier]:
            continue
        score = compare_to_fingerprint(live, clusters[tier]["avg_start"], tier)
        match_scores[tier] = score
        print(f"📊 {tier} match: {score}%")

    for i, tier in enumerate(tiers):
        if match_scores.get(tier, 0) < 70:
            passed = False
        if passed:
            print(f"✅ All tiers up to {tier} aligned → SIGNAL: {tier} move possible ✅")

if __name__ == "__main__":
    match_fingerprint_live()
