#!/usr/bin/env python3
import sys
import csv

if len(sys.argv) < 4:
    print(
        "Usage: compare_statistics.py <stats_old.csv> <stats_new.csv> <statistic_name>..."
    )
    exit(1)

# Read result files
old = {}
with open(sys.argv[1], newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        columns = []
        for stat in sys.argv[3:]:
            columns.append(row[stat])
        old[(row["problem"], row["data_file"])] = columns
new = {}
with open(sys.argv[2], newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        columns = []
        for stat in sys.argv[3:]:
            columns.append(row[stat])
        new[(row["problem"], row["data_file"])] = columns

# Select Matching rows
keys = ["problem", "data_file"]
for stat in sys.argv[3:]:
    keys.extend([f"old_{stat}", f"new_{stat}"])

writer = csv.DictWriter(sys.stdout, keys, dialect="unix", extrasaction="ignore")
writer.writeheader()
for key, val in old.items():
    if key in new:
        row = {
            "problem": key[0],
            "data_file": key[1],
        }
        for i in range(len(val)):
            row[f"old_{sys.argv[3+i]}"] = val[i]
            row[f"new_{sys.argv[3+i]}"] = new[key][i]
        writer.writerow(row)
