import pandas as pd

df = pd.read_csv("edited_bgp_updates.csv")

# ASNs relevant to the Cloudflare incident
interesting_asns = ["267613", "262504", "53072", "7738", "13335"]

def path_contains_interesting_asn(path: str) -> bool:
    if not isinstance(path, str):
        return False
    parts = path.split()
    return any(asn in parts for asn in interesting_asns)

df_asn = df[df["as_path"].apply(path_contains_interesting_asn)].copy()

df_asn["origin_as"] = df_asn["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

print("=== Rows containing Cloudflare-related ASNs ===")
print(df_asn.head(50))
print("\nTotal rows:", len(df_asn))

print("\nTop prefixes:")
print(df_asn["prefix"].value_counts().head(20))

print("\nTop AS paths:")
print(df_asn["as_path"].value_counts().head(20))

print("\nTop origin AS values:")
print(df_asn["origin_as"].value_counts().head(20))

print("\nSource files:")
print(df_asn["source_file"].value_counts())

df_asn.to_csv("cloudflare_asn_results.csv", index=False)
print("\nSaved to cloudflare_asn_results.csv")