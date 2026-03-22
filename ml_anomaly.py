import pandas as pd
from sklearn.ensemble import IsolationForest

df = pd.read_csv("prefix_features.csv")

features = df[["updates", "avg_path_len", "max_path_len", "min_path_len", "unique_origins"]]

model = IsolationForest(contamination=0.02, random_state=42)
df["anomaly"] = model.fit_predict(features)

# -1 = anomaly, 1 = normal
anomalies = df[df["anomaly"] == -1]

print("Detected anomalies:")
print(anomalies.head(20))

anomalies.to_csv("detected_anomalies.csv", index=False)
print("\nSaved anomalies to detected_anomalies.csv")