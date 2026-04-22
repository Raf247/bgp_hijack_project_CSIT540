import pandas as pd

df = pd.read_csv("edited_bgp_updates.csv")

# Focus only on leaked Cloudflare /24
df_leak = df[df["prefix"] == "1.1.1.0/24"].copy()

# Extract origin AS
df_leak["origin_as"] = df_leak["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

print("=== Cloudflare Route Leak Test (1.1.1.0/24) ===")
print(df_leak.head(30))
print("\nTotal rows:", len(df_leak))

print("\nUnique origin AS values:")
print(df_leak["origin_as"].value_counts(dropna=False))

print("\nUnique AS paths:")
print(df_leak["as_path"].value_counts(dropna=False))

print("\nPath length distribution:")
print(df_leak["path_length"].value_counts(dropna=False).sort_index())

print("\nSource files:")
print(df_leak["source_file"].value_counts(dropna=False))

# Optional: save results
df_leak.to_csv("cloudflare_leak_results.csv", index=False)
print("\nSaved to cloudflare_leak_results.csv")