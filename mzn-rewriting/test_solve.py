#!/usr/bin/env python3
import minizinc
import sys
import os
import re
import time
import subprocess
from pathlib import Path

MZNCC = "/Users/jdek0001/Dropbox/development/minizinc.byte/build/Release/mzncc"
MZNASM = "/Users/jdek0001/Dropbox/development/minizinc.byte/build/Release/mznasm"

# Instances Selection (File location)
if len(sys.argv) < 4:
    print("Usage: test_solve.py <solver/library> <output_var> <model> <data_file>?")
    exit(1)

solver = sys.argv[1]
outputvar = sys.argv[2]
model = Path(sys.argv[3])
data = None
if len(sys.argv) > 4:
    data = Path(sys.argv[4])

# Extend model with `output_this`
model_bin = model.read_bytes()
model_bin += bytes(f"constraint output_this({outputvar});", encoding='utf8')
Path("_temp.mzn").write_bytes(model_bin)

# Compile model using MZNCC
os.system(f"{MZNCC} -G{solver} _temp.mzn > _temp.uzn")

# Flatten/Run model using MZNASM
cmd = [
    MZNASM,
    "--solver",
    solver,
    "-t",
    str(20000),
    "-f",
    "_temp.uzn",
]
if data:
    cmd.append(data)
output = subprocess.run(cmd, capture_output=True,)
if output.stderr:
    print(f"mznasm stderr:\n {output.stderr.decode('utf-8')}")
if b"=====ERROR=====" in output.stdout:
    print("=====ERROR=====")
    exit(1)
elif b"=====UNKNOWN=====" in output.stdout:
    print("=====UNKNOWN=====")
    exit(1)
elif b"=====UNSATISFIABLE=====" in output.stdout:
    print("=====UNSATISFIABLE=====")
    exit(1)
elif (b"=====UNSATorUNBOUNDED=====" in output.stdout or b"=====UNBOUNDED=====" in output.stdout):
    print("=====UNSATISFIABLE=====")
    exit(1)

filtered = re.sub(
    rb"^-{10}|={5}(ERROR|UNKNOWN|UNSATISFIABLE|UNSATorUNBOUNDED|UNBOUNDED|)?={5}",
    b"",
    output.stdout,
    flags=re.MULTILINE,
)
filtered = re.sub(rb"^\w*%.*\n?", b"", filtered, flags=re.MULTILINE)

if output.returncode != 0:
    print(
        f"mznasm ({cmd}) ERROR {output.returncode}: \n{str(output.stderr)}\n",
        file=sys.stderr,
    )
    exit(1)

gecode = minizinc.Solver.lookup("gecode")
check_inst = minizinc.Instance(gecode)
check_inst.add_file(model)
if data:
    check_inst.add_file(data, parse_data=False)

check_inst.add_string(f"constraint {outputvar} = {filtered.decode('utf-8')};")

sol = check_inst.solve()
print(f"Status: {sol.status}")
print(sol)
