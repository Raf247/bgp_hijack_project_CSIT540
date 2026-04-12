import bz2
import csv
import os
from mrtparse import Reader

DATA_DIR = "../data"
OUTPUT_FILE = "edited_bgp_updates.csv"

files_to_process = [
    "updates.20240627.1815.bz2",
    "updates.20240627.1830.bz2",
    "updates.20240627.1845.bz2",
    "updates.20240627.1900.bz2",
    "updates.20240627.1915.bz2",
    "updates.20240627.1930.bz2",
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow(["timestamp", "prefix", "as_path", "path_length", "source_file"])

    total_count = 0

    for filename in files_to_process:
        filepath = os.path.join(DATA_DIR, filename)
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
                                    filename
                                ])
                                file_count += 1
                                total_count += 1

                    except Exception:
                        continue

            print(f"Finished {filename}: {file_count} entries")

        except Exception as e:
            print(f"Failed on {filename}: {e}")

print(f"Done. Total parsed entries: {total_count}")