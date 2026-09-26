"""
The two implementations, compared.

`smprime.core` explores states proposer-side by depth-first search from the
definition of the algorithm.  `smprime.altcore` was written separately: it
encodes a state receiver-side, explores breadth-first with an explicit
queue, keeps receiver preferences as rank matrices, and recomputes the
active set from the holder vector rather than from the matching.  They share
no code.  If they disagree on any instance, one of them is wrong.

    python scripts/crosscheck.py            size three exhaustively, then
                                            samples at sizes four and five
    python scripts/crosscheck.py 4 500      500 random instances of size four
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smprime import altcore, core, families


def both(P, R):
    states, arcs, term = core.reachable(P, R)
    adj = altcore.reachable_graph(altcore.Instance(P, R))
    ends = [s for s, o in adj.items() if not o]
    return ((len(states), arcs, term[1]),
            (len(adj), sum(len(o or {}) for o in adj.values()),
             ends[0][1] if len(ends) == 1 else None))


def sweep(n, trials=None, seed=0):
    if trials is None:
        cases = families.all_instances(n)
    else:
        rng = random.Random(seed)
        cases = (families.random_instance(rng, n) for _ in range(trials))
    bad = done = 0
    for P, R in cases:
        a, b = both(P, R)
        done += 1
        if a != b:
            bad += 1
            if bad <= 3:
                print("   disagreement: P=%s R=%s  %s vs %s" % (P, R, a, b))
    print("  size %d: %s instances, %d disagreements  %s"
          % (n, format(done, ","), bad, "PASS" if bad == 0 else "FAIL"))
    return bad


if __name__ == "__main__":
    if len(sys.argv) == 3:
        sys.exit(1 if sweep(int(sys.argv[1]), int(sys.argv[2])) else 0)
    print("comparing the two implementations")
    bad = sweep(3) + sweep(4, 2000, 1) + sweep(5, 300, 2)
    sys.exit(1 if bad else 0)
