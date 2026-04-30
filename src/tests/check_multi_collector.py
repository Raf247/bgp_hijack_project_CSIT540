import pandas as pd

# Path from src/tests → results/csv
df = pd.read_csv("../../results/csv/cloudflare_multi_collector_updates.csv")

print("=== BASIC INFO ===")
print("Total rows:", len(df))

print("\n=== ROWS PER COLLECTOR ===")
print(df["collector"].value_counts())

print("\n=== EXACT CLOUDFLARE PREFIX (1.1.1.0/24) ===")
df_cf = df[df["prefix"] == "1.1.1.0/24"]
print(df_cf["collector"].value_counts())

print("\n=== CHECK FOR HIJACK PREFIX (1.1.1.1/32) ===")
df_hijack = df[df["prefix"] == "1.1.1.1/32"]
print("Total rows:", len(df_hijack))
print(df_hijack.head())

print("\n=== UNIQUE ORIGIN AS PER COLLECTOR ===")
df["origin_as"] = df["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

print(df.groupby("collector")["origin_as"].nunique())

print("\n=== HIJACK VISIBILITY PER COLLECTOR ===")
print(df[df["prefix"] == "1.1.1.1/32"]["collector"].value_counts())