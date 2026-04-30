import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# =========================
# Load raw multi-collector data
# =========================
df = pd.read_csv("../../results/csv/cloudflare_multi_collector_updates.csv")

# Extract clean timestamp from format like {1719514377: '2024-06-27 14:52:57'}
df["timestamp"] = df["timestamp"].astype(str).str.extract(r"'([^']+)'")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Extract origin AS from AS path
df["origin_as"] = df["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

# Drop rows with bad timestamps
df = df.dropna(subset=["timestamp"])

# =========================
# Build time-window features
# =========================
df_grouped = (
    df.groupby(pd.Grouper(key="timestamp", freq="5min"))
    .agg(
        updates=("prefix", "count"),
        avg_path_len=("path_length", "mean"),
        max_path_len=("path_length", "max"),
        min_path_len=("path_length", "min"),
        unique_origins=("origin_as", "nunique"),
        unique_prefixes=("prefix", "nunique"),
        unique_collectors=("collector", "nunique"),
    )
    .reset_index()
)

# Remove empty time windows
df_grouped = df_grouped[df_grouped["updates"] > 0].copy()

# =========================
# Select ML features
# =========================
features = [
    "updates",
    "avg_path_len",
    "max_path_len",
    "min_path_len",
    "unique_origins",
    "unique_prefixes",
    "unique_collectors",
]

X = df_grouped[features].fillna(0)

# Remove duplicate feature rows to reduce LOF warning
X = X.drop_duplicates()
df_grouped = df_grouped.loc[X.index].copy()

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# 1. Isolation Forest
# =========================
iso = IsolationForest(contamination=0.05, random_state=42)
df_grouped["iso_anomaly"] = iso.fit_predict(X_scaled)

# =========================
# 2. Local Outlier Factor
# =========================
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
df_grouped["lof_anomaly"] = lof.fit_predict(X_scaled)

# =========================
# 3. DBSCAN
# =========================
dbscan = DBSCAN(eps=1.5, min_samples=5)
df_grouped["dbscan_cluster"] = dbscan.fit_predict(X_scaled)
df_grouped["dbscan_anomaly"] = df_grouped["dbscan_cluster"].apply(
    lambda x: -1 if x == -1 else 1
)

# =========================
# Combine model outputs
# =========================
df_grouped["combined_anomaly"] = (
    (df_grouped["iso_anomaly"] == -1)
    | (df_grouped["lof_anomaly"] == -1)
    | (df_grouped["dbscan_anomaly"] == -1)
)

# =========================
# Show results
# =========================
print("\n=== ANOMALY SUMMARY ===")
print("Isolation Forest:", (df_grouped["iso_anomaly"] == -1).sum())
print("LOF:", (df_grouped["lof_anomaly"] == -1).sum())
print("DBSCAN:", (df_grouped["dbscan_anomaly"] == -1).sum())
print("Combined:", df_grouped["combined_anomaly"].sum())

print("\n=== ANOMALOUS TIME WINDOWS ===")
print(df_grouped[df_grouped["combined_anomaly"] == True].head(30))

# =========================
# Cloudflare incident window check
# =========================
incident_start = pd.Timestamp("2024-06-27 18:45:00")
incident_end = pd.Timestamp("2024-06-27 20:15:00")

incident_windows = df_grouped[
    (df_grouped["timestamp"] >= incident_start)
    & (df_grouped["timestamp"] <= incident_end)
].copy()

print("\n=== CLOUDFLARE INCIDENT WINDOW ===")
print(incident_windows)

print("\n=== ANOMALIES DURING CLOUDFLARE INCIDENT WINDOW ===")
print(incident_windows[incident_windows["combined_anomaly"] == True])

# =========================
# Save results
# =========================
df_grouped.to_csv("../../results/csv/multi_model_time_anomalies.csv", index=False)

print("\nSaved to multi_model_time_anomalies.csv")