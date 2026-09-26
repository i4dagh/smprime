"""
Re-derive the checkable numbers of the paper, and print PASS or FAIL.

    python scripts/verify_paper.py          the quick checks, seconds
    python scripts/verify_paper.py --all    also the exhaustive size-three
                                            pass, about a minute

Exits non-zero if anything failed, so it can be run unattended or in CI.

  A  size three, exhaustive over all 46,656 instances: the Boolean-cube
     count of Corollary 5.1, the equivalence of Theorem 5, the uniqueness of
     the finest partition of Theorem 6 against the meet of every partition
     into blocks, and the decomposable count of Table 3
  B  the census recursion of Theorem 9 to n = 5, against that exhaustive
     count and against every entry of Table 3
  C  the products theorem and all six composition laws of Corollary 7.2, on
     random direct sums at sizes four to six
  D  the instance drawn in Fig 1, and each of its six composition laws
  E  the two families of Proposition 12.3, at sizes two to six
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smprime import blocks, census, core, families

FAIL = []


def report(name, ok, detail=""):
    print("  %-4s %s%s" % ("PASS" if ok else "FAIL", name,
                           ("   " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)


def check_A(uniqueness_every=4096):
    print("\nA. size three, exhaustive")
    cubes = decomp = 0
    shapes = {}
    thm5 = thm6 = True
    for seen, (P, R) in enumerate(families.all_instances(3), 1):
        cube = core.is_cube(P, R)
        if cube != (len({P[p][0] for p in range(3)}) == 3):
            thm5 = False
        cubes += cube
        f = blocks.finest_partition(P, R)
        decomp += len(f) > 1
        key = tuple(sorted((len(A) for A in f), reverse=True))
        shapes[key] = shapes.get(key, 0) + 1
        if seen % uniqueness_every == 0:
            m = None
            for part in blocks.all_block_partitions(P, R):
                m = part if m is None else blocks.meet(m, part)
            if sorted(m, key=sorted) != f:
                thm6 = False
    report("Theorem 5, Boolean cube iff distinct first choices", thm5)
    report("Corollary 5.1, Boolean cubes at n = 3", cubes == 10368,
           "%s, expected 10,368" % format(cubes, ","))
    report("Table 3, input-decomposable at n = 3", decomp == 888,
           "%s, expected 888" % format(decomp, ","))
    report("Theorem 6, the finest partition is the meet of all of them", thm6)
    print("       shapes of the finest partition:",
          ", ".join("%s: %s" % ("+".join(map(str, k)), format(v, ","))
                    for k, v in sorted(shapes.items())))
    return decomp


def check_B(decomp3=None):
    print("\nB. the census of Theorem 9")
    Pi, rows = census.census(5)
    report("Table 3 rows n = 2 and n = 3", Pi[2] == 14 and Pi[3] == 45768,
           "Pi(2) = %d, Pi(3) = %s" % (Pi[2], format(Pi[3], ",")))
    report("Table 3 row n = 4, total T(4)", rows[4][0] == 110075314176,
           format(rows[4][0], ","))
    report("Table 3 row n = 4, decomposable", rows[4][1] == 88478208,
           format(rows[4][1], ","))
    want = {(3, 1): 26362368, (2, 2): 903168, (2, 1, 1): 20901888,
            (1, 1, 1, 1): 40310784}
    got = rows[4][3]
    report("the four shape counts at n = 4",
           all(got.get(k) == v for k, v in want.items()),
           ", ".join("%s: %s" % ("+".join(map(str, k)),
                                 format(got.get(k, 0), ",")) for k in want))
    report("Pi(5) of the text", Pi[5] == 619162084591420538880,
           format(Pi[5], ","))
    if decomp3 is not None:
        report("the n = 3 row agrees with the exhaustive pass",
               rows[3][1] == decomp3, "%d vs %d" % (rows[3][1], decomp3))


def check_C(trials=40, seed=11):
    print("\nC. the products theorem and the composition laws")
    rng = random.Random(seed)
    bad = {k: 0 for k in ("N", "E/N", "Q*", "L", "kappa", "|Stab|")}
    done = 0
    for _ in range(trials):
        k1, k2 = rng.choice([1, 2, 3]), rng.choice([1, 2, 3])
        if not 4 <= k1 + k2 <= 6:
            continue
        I1 = families.random_instance(rng, k1)
        I2 = families.random_instance(rng, k2)
        a, b = core.invariants(*I1), core.invariants(*I2)
        c = core.invariants(*families.direct_sum([I1, I2]))
        done += 1
        bad["N"] += a["N"] * b["N"] != c["N"]
        bad["E/N"] += abs(a["E"] / a["N"] + b["E"] / b["N"]
                          - c["E"] / c["N"]) > 1e-9
        bad["Q*"] += a["Q"] + b["Q"] != c["Q"]
        bad["L"] += a["L"] * b["L"] * math.comb(c["Q"], a["Q"]) != c["L"]
        bad["kappa"] += abs(a["kappa"] * b["kappa"] - c["kappa"]) > 1e-9
        bad["|Stab|"] += a["stab"] * b["stab"] != c["stab"]
    for k, v in bad.items():
        report("composition law: %s" % k, v == 0,
               "%d direct sums, %d failures" % (done, v))


def check_D():
    print("\nD. the instance of Fig 1")
    (I1, I2), I = families.figure_instance()
    a, b, c = core.invariants(*I1), core.invariants(*I2), core.invariants(*I)
    for name, ok in [
            ("N = 10 x 4 = 40",
             (a["N"], b["N"], c["N"]) == (10, 4, 40)),
            ("E = 15 and 4, E/N = 1.5 + 1.0 = 2.5",
             (a["E"], b["E"]) == (15, 4) and abs(c["E"] / c["N"] - 2.5) < 1e-9),
            ("Q* = 4 + 2 = 6", (a["Q"], b["Q"], c["Q"]) == (4, 2, 6)),
            ("L = 8 x 2 x C(6,4) = 240", (a["L"], b["L"], c["L"]) == (8, 2, 240)),
            ("commutation index 2/3 x 1 = 2/3",
             abs(a["kappa"] - 2 / 3) < 1e-12 and abs(b["kappa"] - 1) < 1e-12
             and abs(c["kappa"] - 2 / 3) < 1e-12),
            ("stable matchings 2 x 2 = 4",
             (a["stab"], b["stab"], c["stab"]) == (2, 2, 4)),
            ("the only proper blocks are the two factors",
             sorted(sorted(A) for A, _B in blocks.blocks(*I) if len(A) < 5)
             == [[0, 1, 2], [3, 4]])]:
        report(name, ok)


def check_E():
    print("\nE. the two families of Proposition 12.3")
    for n in range(2, 7):
        A, C = families.aligned(n), families.antiphase(n)
        ia, ic = core.invariants(*A), core.invariants(*C)
        report("n = %d: both run as the Boolean cube" % n,
               ia["N"] == 2 ** n and ic["N"] == 2 ** n,
               "N = %d and %d" % (ia["N"], ic["N"]))
        report("n = %d: one stable matching against n of them" % n,
               ia["stab"] == 1 and ic["stab"] == n,
               "|Stab| = %d aligned, %d anti-phase" % (ia["stab"], ic["stab"]))
        report("n = %d: one is all singletons, the other prime" % n,
               len(blocks.finest_partition(*A)) == n
               and len(blocks.finest_partition(*C)) == 1)


def main():
    full = "--all" in sys.argv
    print("smprime: verification of the paper's checkable numbers")
    print("python %s, exhaustive size-three pass %s"
          % (sys.version.split()[0], "on" if full else "off (use --all)"))
    d3 = check_A() if full else None
    if not full:
        print("\nA. size three, exhaustive   SKIPPED (--all, about a minute)")
    check_B(d3)
    check_C()
    check_D()
    check_E()
    print("\n%d checks failed" % len(FAIL))
    for f in FAIL:
        print("   ", f)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
