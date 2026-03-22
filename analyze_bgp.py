import pandas as pd

df = pd.read_csv("bgp_updates.csv")

df["origin_as"] = df["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

prefix_stats = df.groupby("prefix").agg(
    updates=("prefix", "count"),
    avg_path_len=("path_length", "mean"),
    unique_origins=("origin_as", "nunique")
).reset_index()

print(prefix_stats.head(20))