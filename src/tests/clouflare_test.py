import pandas as pd

df = pd.read_csv("../../results/csv/edited_bgp_updates.csv")

# Exact incident prefixes
target_prefixes = ["1.1.1.0/24", "1.1.1.1/32"]

df_target = df[df["prefix"].isin(target_prefixes)].copy()

# Extract origin AS
df_target["origin_as"] = df_target["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

print("=== Exact Cloudflare Incident Prefixes ===")
print(df_target.head(30))
print("\nTotal rows:", len(df_target))

print("\nUnique prefixes:")
print(df_target["prefix"].value_counts(dropna=False))

print("\nUnique origin AS values:")
print(df_target["origin_as"].value_counts(dropna=False))

print("\nUnique AS paths:")
print(df_target["as_path"].value_counts(dropna=False))

print("\nSource files:")
print(df_target["source_file"].value_counts(dropna=False))

# Optional: save results
df_target.to_csv("cloudflare_exact_results.csv", index=False)
print("\nSaved to cloudflare_exact_results.csv")