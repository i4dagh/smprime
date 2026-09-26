"""
The size-three atlas: every instance, with its invariants.

At size three there are 46,656 instances with strict complete preferences on
both sides, and all of them fit in one table.  This script writes that table,
so that a question about small instances can be answered by a query rather
than by a new program.

    python scripts/size3_dataset.py           writes data/size3.csv.gz
    python scripts/size3_dataset.py --plain   writes data/size3.csv

Columns

    P, R        the two preference matrices, flattened, best first, so that
                "012,120,201" is proposer 0 ranking r0 r1 r2, proposer 1
                ranking r1 r2 r0, and so on
    N           reachable states
    E           arcs of the reachable state graph
    Qstar       proposals made in total
    L           complete schedules
    kappa       L divided by the multinomial of the terminal pointer vector,
                so 1 exactly on the Boolean cube
    stab        stable matchings
    shape       the block forest up to relabelling, "3(1 1)" meaning two
                singleton blocks inside the whole
    parts       sizes of the finest partition, "1+1+1" or "2+1" or "3"
    prime       1 when the instance is input-prime, 0 when it decomposes
    cube        1 when the state graph is the Boolean cube

Runtime is a few minutes; the work is the brute-force stable-matching sweep
and the path count, both of which recompute from the definitions.
"""
import csv
import gzip
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from smprime import blocks, core, families

FIELDS = ["P", "R", "N", "E", "Qstar", "L", "kappa", "stab", "shape",
          "parts", "prime", "cube"]


def flat(M):
    return ",".join("".join(str(x) for x in row) for row in M)


def rows():
    for P, R in families.all_instances(3):
        inv = core.invariants(P, R)
        f = blocks.finest_partition(P, R)
        yield {
            "P": flat(P), "R": flat(R),
            "N": inv["N"], "E": inv["E"], "Qstar": inv["Q"], "L": inv["L"],
            "kappa": "%.10f" % inv["kappa"], "stab": inv["stab"],
            "shape": blocks.show_shape(blocks.forest_shape(P, R)),
            "parts": "+".join(str(len(A))
                              for A in sorted(f, key=lambda s: -len(s))),
            "prime": 0 if len(f) > 1 else 1,
            "cube": 1 if inv["N"] == 8 else 0,
        }


def main():
    plain = "--plain" in sys.argv
    out = os.path.join(ROOT, "data", "size3.csv" + ("" if plain else ".gz"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    opener = open if plain else gzip.open
    t0, n = time.time(), 0
    with opener(out, "wt", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for row in rows():
            w.writerow(row)
            n += 1
            if n % 10000 == 0:
                print("  %s rows, %.0f s" % (format(n, ","), time.time() - t0),
                      flush=True)
    print("wrote %s: %s rows in %.0f s"
          % (out, format(n, ","), time.time() - t0))
    if n != 46656:
        raise SystemExit("expected 46,656 rows, wrote %d" % n)


if __name__ == "__main__":
    main()
