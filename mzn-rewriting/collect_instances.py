import csv
import os
import sys
from pathlib import Path

assert len(sys.argv) >= 2
benchmarks_location = sys.argv[1]

writer = csv.writer(sys.stdout, dialect="unix")
writer.writerow(("problem", "model", "data_file"))
for root, _, files in os.walk(benchmarks_location):
    for name in files:
        if name.endswith(".mzn"):
            problem = root.split(os.sep)[-1]
            datafiles = 0
            for nroot, _, nfiles in os.walk(root):
                for nname in nfiles:
                    if nname.endswith(".dzn") or nname.endswith(".json"):
                        datafiles = datafiles + 1
                        writer.writerow(
                            (
                                problem,
                                Path(root + "/" + name),
                                Path(nroot + "/" + nname),
                            )
                        )

            if datafiles == 0:
                writer.writerow((problem, Path(root + "/" + name), ""))
