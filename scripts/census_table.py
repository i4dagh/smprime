"""
Print the exact census of input-prime instances, and write it as CSV.

    python scripts/census_table.py [nmax]      default 8

Writes data/census.csv with one row per size: the number of instances, how
many of them decompose, how many are prime, and the decomposable fraction.
The counts are exact integers; only the fraction is a float.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from smprime import census

nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
rows = census.table(nmax)
print("%2s  %-26s %-24s %-26s %s"
      % ("n", "instances T(n)", "decomposable", "input-prime Pi(n)", "fraction"))
for r in rows:
    print("%2d  %-26s %-24s %-26s %.4e"
          % (r["n"], format(r["T"], ","), format(r["decomposable"], ","),
             format(r["prime"], ","), r["fraction"]))
print("\nthe decomposable fraction is asymptotically n!/n^(2n)")
out = os.path.join(HERE, "data", "census.csv")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["n", "instances", "decomposable", "prime", "fraction"])
    for r in rows:
        w.writerow([r["n"], r["T"], r["decomposable"], r["prime"],
                    "%.6e" % r["fraction"]])
print("wrote", out)
