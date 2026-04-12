import pandas as pd

df = pd.read_csv("edited_bgp_updates.csv")

# Broader Cloudflare-related neighborhood
df_broad = df[df["prefix"].astype(str).str.startswith("1.1.")].copy()

df_broad["origin_as"] = df_broad["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

print("Total broad rows:", len(df_broad))
print("\nTop prefixes:")
print(df_broad["prefix"].value_counts().head(20))
print("\nTop origin AS values:")
print(df_broad["origin_as"].value_counts().head(20))