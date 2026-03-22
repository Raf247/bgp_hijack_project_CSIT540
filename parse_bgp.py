import bz2
import csv
from mrtparse import Reader

input_file = "data/updates.20260301.0000.bz2"
output_file = "bgp_updates.csv"

with bz2.open(input_file, "rb") as f, open(output_file, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow(["timestamp", "prefix", "as_path", "path_length"])

    count = 0

    for entry in Reader(f):
        if entry.err:
            continue

        data = entry.data

        # Make sure this record contains a BGP message
        if "bgp_message" not in data:
            continue

        bgp_msg = data["bgp_message"]

        # We only want UPDATE messages
        if "type" not in bgp_msg or "UPDATE" not in str(bgp_msg["type"]):
            continue

        timestamp = data.get("timestamp", None)
        nlri_list = bgp_msg.get("nlri", [])
        path_attrs = bgp_msg.get("path_attributes", [])

        # Extract AS_PATH
        as_path_parts = []
        for attr in path_attrs:
            attr_type = attr.get("type", "")
            if "AS_PATH" in str(attr_type):
                for segment in attr.get("value", []):
                    segment_value = segment.get("value", [])
                    as_path_parts.extend(segment_value)

        as_path = " ".join(as_path_parts)
        path_length = len(as_path_parts)

        # Extract prefixes
        for nlri in nlri_list:
            prefix = nlri.get("prefix", None)
            if prefix:
                writer.writerow([timestamp, prefix, as_path, path_length])
                count += 1

print(f"Done. Parsed {count} entries.")