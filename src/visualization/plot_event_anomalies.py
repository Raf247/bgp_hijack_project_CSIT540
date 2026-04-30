import pandas as pd
import matplotlib.pyplot as plt

# =========================
# File paths
# =========================
cloudflare_file = "../../results/csv/multi_model_time_anomalies.csv"
facebook_file = "../../results/csv/facebook_multi_model_time_anomalies.csv"

# =========================
# Load data
# =========================
cf = pd.read_csv(cloudflare_file)
fb = pd.read_csv(facebook_file)

cf["timestamp"] = pd.to_datetime(cf["timestamp"])
fb["timestamp"] = pd.to_datetime(fb["timestamp"])

# Convert True/False to 1/0 for plotting
cf["anomaly_flag"] = cf["combined_anomaly"].astype(int)
fb["anomaly_flag"] = fb["combined_anomaly"].astype(int)

# =========================
# Graph 1: Cloudflare anomalies over time
# =========================
plt.figure(figsize=(10, 5))
plt.plot(cf["timestamp"], cf["updates"], marker="o", label="BGP Updates")
plt.scatter(
    cf[cf["combined_anomaly"] == True]["timestamp"],
    cf[cf["combined_anomaly"] == True]["updates"],
    marker="x",
    s=100,
    label="Detected Anomaly"
)

plt.axvspan(
    pd.Timestamp("2024-06-27 15:00:00"),
    pd.Timestamp("2024-06-27 17:30:00"),
    alpha=0.2,
    label="Cloudflare Incident Window"
)

plt.title("Cloudflare 2024: BGP Updates and Detected Anomalies")
plt.xlabel("Time")
plt.ylabel("Number of Updates")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("../../results/graphs/cloudflare_anomalies_over_time.png")
plt.show()

# =========================
# Graph 2: Facebook anomalies over time
# =========================
plt.figure(figsize=(10, 5))
plt.plot(fb["timestamp"], fb["updates"], marker="o", label="BGP Updates")
plt.scatter(
    fb[fb["combined_anomaly"] == True]["timestamp"],
    fb[fb["combined_anomaly"] == True]["updates"],
    marker="x",
    s=100,
    label="Detected Anomaly"
)

plt.axvspan(
    pd.Timestamp("2021-10-04 11:30:00"),
    pd.Timestamp("2021-10-04 13:30:00"),
    alpha=0.2,
    label="Facebook Incident Window"
)

plt.title("Facebook 2021: BGP Updates and Detected Anomalies")
plt.xlabel("Time")
plt.ylabel("Number of Updates")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("../../results/graphs/facebook_anomalies_over_time.png")
plt.show()

# =========================
# Graph 3: Model comparison
# =========================
model_summary = pd.DataFrame({
    "Event": ["Cloudflare", "Facebook"],
    "Isolation Forest": [
        (cf["iso_anomaly"] == -1).sum(),
        (fb["iso_anomaly"] == -1).sum()
    ],
    "LOF": [
        (cf["lof_anomaly"] == -1).sum(),
        (fb["lof_anomaly"] == -1).sum()
    ],
    "DBSCAN": [
        (cf["dbscan_anomaly"] == -1).sum(),
        (fb["dbscan_anomaly"] == -1).sum()
    ],
    "Combined": [
        cf["combined_anomaly"].sum(),
        fb["combined_anomaly"].sum()
    ]
})

model_summary.set_index("Event").plot(kind="bar", figsize=(9, 5))
plt.title("ML Model Anomaly Detection Comparison")
plt.xlabel("Incident")
plt.ylabel("Number of Detected Anomaly Windows")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("../../results/graphs/model_comparison.png")
plt.show()

print("Saved graphs:")
print("- cloudflare_anomalies_over_time.png")
print("- facebook_anomalies_over_time.png")
print("- model_comparison.png")