import bz2
import csv
import os
from mrtparse import Reader

DATA_DIR = "../data"
OUTPUT_FILE = "edited_bgp_updates.csv"

files_to_process = [
    "updates.20240627.0000.bz2",
    "updates.20240627.0015.bz2",
    "updates.20240627.0030.bz2",
    "updates.20240627.0045.bz2",
    "updates.20240627.0100.bz2",
    "updates.20240627.0115.bz2",
    "updates.20240627.0130.bz2",
    "updates.20240627.0145.bz2",
    "updates.20240627.0200.bz2",
    "updates.20240627.0215.bz2",
    "updates.20240627.0230.bz2",
    "updates.20240627.0245.bz2",
    "updates.20240627.0300.bz2",
    "updates.20240627.0315.bz2",
    "updates.20240627.0330.bz2",
    "updates.20240627.0345.bz2",
    "updates.20240627.0400.bz2",
    "updates.20240627.0415.bz2",
    "updates.20240627.0430.bz2",
    "updates.20240627.0445.bz2",
    "updates.20240627.0500.bz2",
    "updates.20240627.0515.bz2",
    "updates.20240627.0530.bz2",
    "updates.20240627.0545.bz2",
    "updates.20240627.0600.bz2",
    "updates.20240627.0615.bz2",
    "updates.20240627.0630.bz2",
    "updates.20240627.0645.bz2",
    "updates.20240627.0700.bz2",
    "updates.20240627.0715.bz2",
    "updates.20240627.0730.bz2",
    "updates.20240627.0745.bz2",
    "updates.20240627.0800.bz2",
    "updates.20240627.0815.bz2",
    "updates.20240627.0830.bz2",
    "updates.20240627.0845.bz2",
    "updates.20240627.0900.bz2",
    "updates.20240627.0915.bz2",
    "updates.20240627.0930.bz2",
    "updates.20240627.0945.bz2",
    "updates.20240627.1000.bz2",
    "updates.20240627.1015.bz2",
    "updates.20240627.1030.bz2",
    "updates.20240627.1045.bz2",
    "updates.20240627.1100.bz2",
    "updates.20240627.1115.bz2",
    "updates.20240627.1130.bz2",
    "updates.20240627.1145.bz2",
    "updates.20240627.1200.bz2",
    "updates.20240627.1215.bz2",
    "updates.20240627.1230.bz2",
    "updates.20240627.1245.bz2",
    "updates.20240627.1300.bz2",
    "updates.20240627.1315.bz2",
    "updates.20240627.1330.bz2",
    "updates.20240627.1345.bz2",
    "updates.20240627.1400.bz2",
    "updates.20240627.1415.bz2",
    "updates.20240627.1430.bz2",
    "updates.20240627.1445.bz2",
    "updates.20240627.1500.bz2",
    "updates.20240627.1515.bz2",
    "updates.20240627.1530.bz2",
    "updates.20240627.1545.bz2",
    "updates.20240627.1600.bz2",
    "updates.20240627.1615.bz2",
    "updates.20240627.1630.bz2",
    "updates.20240627.1645.bz2",
    "updates.20240627.1700.bz2",
    "updates.20240627.1715.bz2",
    "updates.20240627.1730.bz2",
    "updates.20240627.1745.bz2",
    "updates.20240627.1800.bz2",
    "updates.20240627.1815.bz2",
    "updates.20240627.1830.bz2",
    "updates.20240627.1845.bz2",
    "updates.20240627.1900.bz2",
    "updates.20240627.1915.bz2",
    "updates.20240627.1930.bz2",
    "updates.20240627.1945.bz2",
    "updates.20240627.2000.bz2",
    "updates.20240627.2015.bz2",
    "updates.20240627.2030.bz2",
    "updates.20240627.2045.bz2",
    "updates.20240627.2100.bz2",
    "updates.20240627.2115.bz2",
    "updates.20240627.2130.bz2",
    "updates.20240627.2145.bz2",
    "updates.20240627.2200.bz2",
    "updates.20240627.2215.bz2",
    "updates.20240627.2230.bz2",
    "updates.20240627.2245.bz2",
    "updates.20240627.2300.bz2",
    "updates.20240627.2315.bz2",
    "updates.20240627.2330.bz2",
    "updates.20240627.2345.bz2",
    "updates.20240628.0000.bz2",
    "updates.20240628.0015.bz2",
    "updates.20240628.0030.bz2",
    "updates.20240628.0045.bz2",
    "updates.20240628.0100.bz2",
    "updates.20240628.0115.bz2",
    "updates.20240628.0130.bz2",
    "updates.20240628.0145.bz2",
    "updates.20240628.0200.bz2",
    "updates.20240628.0215.bz2",
    "updates.20240628.0230.bz2",
    "updates.20240628.0245.bz2",
    "updates.20240628.0300.bz2",
    
    

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