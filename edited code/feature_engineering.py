import pandas as pd

df = pd.read_csv("edited_bgp_updates.csv")

# Clean AS path
df["as_path"] = df["as_path"].fillna("")
df["origin_as"] = df["as_path"].apply(lambda x: x.split()[-1] if x.strip() else None)

# Basic per-prefix stats
prefix_features = df.groupby("prefix").agg(
    updates=("prefix", "count"),
    avg_path_len=("path_length", "mean"),
    max_path_len=("path_length", "max"),
    min_path_len=("path_length", "min"),
    unique_origins=("origin_as", "nunique")
).reset_index()

# Suspicion score: simple rule-based signal
prefix_features["suspicious"] = (
    (prefix_features["unique_origins"] > 1) |
    (prefix_features["updates"] > prefix_features["updates"].quantile(0.99)) |
    (prefix_features["avg_path_len"] > prefix_features["avg_path_len"].quantile(0.99))
)

print(prefix_features.head(20))
print("\nSuspicious prefixes:")
print(prefix_features[prefix_features["suspicious"]].head(20))

prefix_features.to_csv("edited_prefix_features.csv", index=False)
print("\nSaved to prefix_features.csv")