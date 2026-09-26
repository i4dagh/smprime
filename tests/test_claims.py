"""
The paper's claims as assertions.

    python -m pytest -q            if pytest is installed
    python tests/test_claims.py    otherwise; same checks, same assertions

The slow test, the exhaustive sweep over all 46,656 size-three instances,
runs only when SMPRIME_FULL is set in the environment:

    SMPRIME_FULL=1 python -m pytest -q
"""
import math
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from smprime import blocks, census, core, families


def test_lemma1_state_is_its_pointer_vector():
    """distinct reachable states have distinct pointer vectors"""
    rng = random.Random(0)
    for n in (2, 3, 4):
        for _ in range(20):
            P, R = families.random_instance(rng, n)
            states = core.reachable(P, R)[0]
            assert len({s[1] for s in states}) == len(states)


def test_theorem5_cube_iff_distinct_first_choices():
    rng = random.Random(1)
    for n in (2, 3, 4, 5):
        for _ in range(30):
            P, R = families.random_instance(rng, n)
            distinct = len({P[p][0] for p in range(n)}) == n
            assert core.is_cube(P, R) == distinct


def test_theorem6_finest_partition_is_the_meet():
    """the finest partition is the meet of every partition into blocks"""
    rng = random.Random(2)
    for n in (3, 4):
        for _ in range(40):
            P, R = families.random_instance(rng, n)
            parts = blocks.all_block_partitions(P, R)
            m = None
            for part in parts:
                m = part if m is None else blocks.meet(m, part)
            assert sorted(m, key=sorted) == blocks.finest_partition(P, R)


def test_theorem7_products_and_composition_laws():
    rng = random.Random(3)
    for _ in range(25):
        k1, k2 = rng.choice([1, 2, 3]), rng.choice([1, 2, 3])
        if not 4 <= k1 + k2 <= 6:
            continue
        I1 = families.random_instance(rng, k1)
        I2 = families.random_instance(rng, k2)
        a, b = core.invariants(*I1), core.invariants(*I2)
        c = core.invariants(*families.direct_sum([I1, I2]))
        assert a["N"] * b["N"] == c["N"]
        assert abs(a["E"] / a["N"] + b["E"] / b["N"] - c["E"] / c["N"]) < 1e-9
        assert a["Q"] + b["Q"] == c["Q"]
        assert a["L"] * b["L"] * math.comb(c["Q"], a["Q"]) == c["L"]
        assert abs(a["kappa"] * b["kappa"] - c["kappa"]) < 1e-9
        assert a["stab"] * b["stab"] == c["stab"]


def test_theorem9_census_matches_table3():
    Pi, rows = census.census(5)
    assert Pi[2] == 14
    assert Pi[3] == 45768
    assert rows[4][0] == 110075314176
    assert rows[4][1] == 88478208
    assert rows[4][3][(3, 1)] == 26362368
    assert rows[4][3][(2, 2)] == 903168
    assert rows[4][3][(2, 1, 1)] == 20901888
    assert rows[4][3][(1, 1, 1, 1)] == 40310784
    assert Pi[5] == 619162084591420538880


def test_proposition12_3_two_families():
    for n in range(2, 7):
        A, C = families.aligned(n), families.antiphase(n)
        ia, ic = core.invariants(*A), core.invariants(*C)
        assert ia["N"] == ic["N"] == 2 ** n            # same execution
        assert ia["stab"] == 1 and ic["stab"] == n     # opposite stable sets
        assert len(blocks.finest_partition(*A)) == n   # maximally decomposable
        assert len(blocks.finest_partition(*C)) == 1   # prime


def test_figure_instance():
    (I1, I2), I = families.figure_instance()
    a, b, c = core.invariants(*I1), core.invariants(*I2), core.invariants(*I)
    assert (a["N"], b["N"], c["N"]) == (10, 4, 40)
    assert (a["E"], b["E"], c["E"]) == (15, 4, 100)
    assert (a["Q"], b["Q"], c["Q"]) == (4, 2, 6)
    assert (a["L"], b["L"], c["L"]) == (8, 2, 240)
    assert (a["stab"], b["stab"], c["stab"]) == (2, 2, 4)
    assert sorted(sorted(A) for A, _B in blocks.blocks(*I) if len(A) < 5) \
        == [[0, 1, 2], [3, 4]]


def test_two_implementations_agree():
    from smprime import altcore
    rng = random.Random(4)
    for n in (2, 3, 4):
        for _ in range(40):
            P, R = families.random_instance(rng, n)
            states, arcs, term = core.reachable(P, R)
            adj = altcore.reachable_graph(altcore.Instance(P, R))
            assert len(states) == len(adj)
            assert arcs == sum(len(o or {}) for o in adj.values())
            assert term[1] == [s for s, o in adj.items() if not o][0][1]


def test_size_three_exhaustive():
    """all 46,656 instances: the counts of Corollary 5.1 and Table 3"""
    if not os.environ.get("SMPRIME_FULL"):
        print("skipped (set SMPRIME_FULL=1 to run, about a minute)")
        return
    cubes = decomp = 0
    for P, R in families.all_instances(3):
        cubes += core.is_cube(P, R)
        decomp += len(blocks.finest_partition(P, R)) > 1
    assert cubes == 10368
    assert decomp == 888


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    bad = 0
    for fn in fns:
        try:
            fn()
            print("  PASS %s" % fn.__name__)
        except AssertionError as exc:
            bad += 1
            print("  FAIL %s   %s" % (fn.__name__, exc))
    print("\n%d of %d tests failed" % (bad, len(fns)))
    sys.exit(1 if bad else 0)
