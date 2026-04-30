import pandas as pd
import matplotlib.pyplot as plt

# Updated file path to point to the correct location of the CSV file.
df = pd.read_csv("../../results/csv/edited_bgp_updates.csv")

# --- FIX TIMESTAMP ---
def extract_time(ts):
    try:
        return str(ts).split("'")[1]
    except:
        return None

df["time"] = df["timestamp"].apply(extract_time)
df["time"] = pd.to_datetime(df["time"])

# Extract origin AS
df["origin_as"] = df["as_path"].fillna("").apply(
    lambda x: x.split()[-1] if isinstance(x, str) and x.strip() else None
)

# -------------------------------
# GRAPH 1 — Updates over time
# -------------------------------
df_target = df[df["prefix"] == "1.1.1.0/24"]

updates_time = df_target.groupby(pd.Grouper(key="time", freq="5min")).size()

plt.figure()
updates_time.plot()
plt.title("BGP Updates Over Time (1.1.1.0/24)")
plt.xlabel("Time")
plt.ylabel("Number of Updates")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../../results/graphs/graph_updates_time.png")
plt.show()

# -------------------------------
# GRAPH 2 — AS Path Length over time
# -------------------------------
path_time = df_target.groupby(pd.Grouper(key="time", freq="5min"))["path_length"].mean()

plt.figure()
path_time.plot()
plt.title("Average AS Path Length Over Time (1.1.1.0/24)")
plt.xlabel("Time")
plt.ylabel("Avg Path Length")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../../results/graphs/graph_path_length.png")
plt.show()

# -------------------------------
# GRAPH 3 — Origin AS distribution (broad)
# -------------------------------
df_broad = df[df["prefix"].astype(str).str.startswith("1.1.")]

origin_counts = df_broad["origin_as"].value_counts().head(10)

plt.figure()
origin_counts.plot(kind="bar")
plt.title("Top Origin AS Distribution (1.1.* prefixes)")
plt.xlabel("Origin AS")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../../results/graphs/graph_origin_distribution.png")
plt.show()