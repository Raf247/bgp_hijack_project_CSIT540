import bz2
import csv
import os
from mrtparse import Reader

DATA_SOURCES = {
    "route-views2": "../../data/facebook/route-views2",
    "route-views.sg": "../../data/facebook/route-views.sg",
    "route-views.eqix": "../../data/facebook/route-views.eqix",
}

OUTPUT_FILE = "../../results/csv/facebook_multi_collector_updates.csv"

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow([
        "timestamp",
        "prefix",
        "as_path",
        "path_length",
        "source_file",
        "collector"
    ])

    total_count = 0

    for collector, data_dir in DATA_SOURCES.items():
        print(f"\n=== Processing collector: {collector} ===")

        for filename in os.listdir(data_dir):
            if not filename.endswith(".bz2"):
                continue

            filepath = os.path.join(data_dir, filename)
            print(f"Processing {filename}...")

            file_count = 0

            try:
                with bz2.open(filepath, "rb") as f:
                    for entry in Reader(f):
                        try:
                            if entry.err:
                                continue

                            data = entry.data

                            if "bgp_message" not in data:
                                continue

                            bgp_msg = data["bgp_message"]

                            if "UPDATE" not in str(bgp_msg.get("type", "")):
                                continue

                            timestamp = data.get("timestamp", None)
                            nlri_list = bgp_msg.get("nlri", [])
                            path_attrs = bgp_msg.get("path_attributes", [])

                            as_path_parts = []

                            for attr in path_attrs:
                                if "AS_PATH" in str(attr.get("type", "")):
                                    for seg in attr.get("value", []):
                                        as_path_parts.extend(seg.get("value", []))

                            as_path = " ".join(as_path_parts)
                            path_length = len(as_path_parts)

                            if not as_path.strip():
                                continue

                            for nlri in nlri_list:
                                prefix = nlri.get("prefix", None)
                                prefix_len = nlri.get("length", None)

                                if prefix and prefix_len is not None:
                                    full_prefix = f"{prefix}/{prefix_len}"

                                    writer.writerow([
                                        timestamp,
                                        full_prefix,
                                        as_path,
                                        path_length,
                                        filename,
                                        collector
                                    ])

                                    file_count += 1
                                    total_count += 1

                        except Exception:
                            continue

                print(f"Finished {filename}: {file_count} entries")

            except Exception as e:
                print(f"Failed on {filename}: {e}")

print(f"\nDone. Total parsed entries: {total_count}")