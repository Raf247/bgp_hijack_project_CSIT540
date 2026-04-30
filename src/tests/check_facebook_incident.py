import pandas as pd

df = pd.read_csv("../../results/csv/facebook_multi_collector_updates.csv")

# Facebook ASN
FACEBOOK_ASN = "32934"

df["origin_as"] = df["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

df_fb = df[df["as_path"].astype(str).str.contains(FACEBOOK_ASN)].copy()

print("=== FACEBOOK INCIDENT CHECK ===")
print("Total rows:", len(df))
print("Rows containing AS32934:", len(df_fb))

print("\nRows per collector:")
print(df["collector"].value_counts())

print("\nFacebook-related rows per collector:")
print(df_fb["collector"].value_counts())

print("\nTop Facebook prefixes:")
print(df_fb["prefix"].value_counts().head(20))

print("\nTop Facebook AS paths:")
print(df_fb["as_path"].value_counts().head(20))

df_fb.to_csv("../../results/csv/facebook_as32934_results.csv", index=False)
print("\nSaved to facebook_as32934_results.csv")