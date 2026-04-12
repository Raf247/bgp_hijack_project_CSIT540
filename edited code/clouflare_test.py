import pandas as pd

df = pd.read_csv("edited_bgp_updates.csv")

# Exact Cloudflare target prefixes only
target_prefixes = ["1.1.1.0/24", "1.1.1.1/32"]

df_target = df[df["prefix"].isin(target_prefixes)].copy()

print("Target prefix rows:")
print(df_target.head(20))
print("\nTotal target rows:", len(df_target))

df_target["origin_as"] = df_target["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

print("\nUnique origin AS for exact target:")
print(df_target["origin_as"].value_counts(dropna=False))

print("\nSource files:")
print(df_target["source_file"].value_counts())

print("\nUnique AS paths:")
print(df_target["as_path"].value_counts())