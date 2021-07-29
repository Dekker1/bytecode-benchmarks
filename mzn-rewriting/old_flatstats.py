#!/usr/bin/env python3
import minizinc
import sys
import csv
import os
import time
import subprocess
import re
from tqdm import tqdm
from pathlib import Path
from datetime import timedelta

# Instances Selection (File location)
if len(sys.argv) < 3:
    print("Usage: new_flatstats.py <instances> <library>")
    exit(1)

REPEATS = 10

instances_location = sys.argv[1]
library = sys.argv[2]


def parse_statistics(stdout: bytes, stderr: bytes):
    statistics: Dict[str, StatisticsType] = {}
    matches = re.findall(rb"%%%mzn-stat:? (\w*)=([^\r\n]*)", stdout)
    for m in matches:
        minizinc.result.set_stat(statistics, m[0].decode(), m[1].decode())

    matches = re.findall(rb"([A-Z].*): (.*)\n", stderr)
    for m in matches:
        statistics[m[0].decode()] = m[1].decode()
    return statistics


writer = None
num_lines = sum(1 for line in open(instances_location)) - 1
with open(instances_location) as instances_file:
    with tqdm(total=num_lines*REPEATS, file=sys.stderr) as pbar:
        reader = csv.reader(instances_file, dialect="unix")
        next(reader, None)  # Skip the header line
        mem = ""
        for row in reader:
            assert len(row) == 3
            pbar.set_description(
                "Flattening %s - %s"
                % (row[1].split(os.sep)[-1], row[2].split(os.sep)[-1])
            )

            # Flatten instance
            cmd = [
                '/usr/bin/time',
                '-v',
                'minizinc',
                "--solver",
                "org.minizinc.mzn-fzn",
                "-c",
                "-s",
                row[1],
            ]
            if row[2]:
                cmd.append(row[2])
            for i in range(REPEATS):
                output = subprocess.run(cmd, capture_output=True,)

                if output.returncode != 0:
                    print(
                        f"mznasm ERROR {output.returncode}: {row[1].split(os.sep)[-1]} - {row[2].split(os.sep)[-1]}:\n{output.stderr}",
                        file=sys.stderr,
                    )
                    break 
                else:
                    stats = parse_statistics(output.stdout, output.stderr)
                    stats["problem"] = row[0]
                    stats["model"] = row[1]
                    stats["data_file"] = row[2]
                    stats["iteration"] = i + 1
                    if writer is None:
                        keys = list(
                            set(
                                ["problem", "model", "data_file", "status"]
                                + list(minizinc.result.StdStatisticTypes.keys())
                                + list(stats.keys())
                            )
                        )
                        writer = csv.DictWriter(
                            sys.stdout, keys, dialect="unix", extrasaction="ignore"
                        )
                        writer.writeheader()
                    writer.writerow(stats)
                pbar.update(1)
                sys.stdout.flush()
