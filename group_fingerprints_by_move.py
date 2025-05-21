
# group_fingerprints_by_move.py

import json
import pandas as pd
from collections import defaultdict

# Define tiers (lower bound, upper bound)
TIERS = {
    "2-3%": (2.0, 3.0),
    "3-5%": (3.01, 5.0),
    "5-10%": (5.01, 10.0),
    "10%+": (10.01, 999.0)
}

def average_fingerprints(fingerprints, key):
    accumulator = defaultdict(list)
    for f in fingerprints:
        for k, v in f.get(key, {}).items():
            if pd.notna(v):
                accumulator[k].append(v)

    return {k: round(sum(v) / len(v), 4) for k, v in accumulator.items() if len(v) >= 3}

def group_fingerprints():
    with open("memory/fingerprint_samples_multi_tf.json", "r") as f:
        data = json.load(f)

    clusters = {}

    for tier, (low, high) in TIERS.items():
        tier_group = [entry for entry in data if low <= abs(entry["move_size"]) <= high]
        clusters[tier] = {
            "count": len(tier_group),
            "avg_start": average_fingerprints(tier_group, "start_indicators"),
            "avg_end": average_fingerprints(tier_group, "end_indicators")
        }

    with open("memory/fingerprint_clusters.json", "w") as f:
        json.dump(clusters, f, indent=2)

    print(f"✅ Grouped into {len(clusters)} tiers")
    print("📁 Saved to memory/fingerprint_clusters.json")
    for tier, info in clusters.items():
        print(f" - {tier}: {info['count']} samples")

if __name__ == "__main__":
    group_fingerprints()
