# smprime - the prime structure of stable-matching instances

Serial deferred acceptance, taken apart. An instance of the stable marriage
problem with strict complete preferences has a unique finest partition of its
agents into *prime blocks*, and that one partition simultaneously factors
three things: the digraph of reachable states of the algorithm, the
antimatroid of feasible proposal prefixes, and the lattice of stable
matchings. This repository is the code behind that result - two independent
implementations of the algorithm, the partition, the exact census of prime
instances, and everything needed to check the paper's numbers from scratch.

It is meant to be useful beyond the paper. If you work on stable matching at
small sizes, `data/size3.csv.gz` answers most questions about size three
without writing any code at all, and `smprime` gives you the state graph, the
blocks and the invariants of any instance in three lines.

**Paper.** Y. Ishida, *Prime factorisation of stable-matching instances:
uniqueness, simultaneous products, and an exact census*, arXiv (2026).

## Install

Nothing to install. `smprime` is pure Python 3.8+ and uses only the standard
library. `matplotlib` is needed for the one figure script and for nothing
else.

```bash
git clone https://github.com/<user>/smprime
cd smprime
python tests/test_claims.py        # about ten seconds
```

## Quick start

```python
from smprime import core, blocks, census, families

P, R = families.antiphase(4)           # the cyclic anti-phase instance
core.invariants(P, R)
# {'N': 16, 'E': 32, 'Q': 4, 'L': 24, 'kappa': 1.0, 'stab': 4, ...}

blocks.finest_partition(P, R)          # prime: one part
# [frozenset({0, 1, 2, 3})]

A = families.aligned(4)                # the same execution, opposite input
blocks.finest_partition(*A)            # four singleton blocks
core.invariants(*A)["stab"]            # 1

census.census(6)[0][6]                 # prime instances of size six
# 19408402087860720702047512795545600
```

`core` recomputes everything from the definitions and never caches, which is
what makes it usable as a check on faster code. `altcore` is a second
implementation, written to be unlike the first: it encodes a state
receiver-side, explores breadth-first, and keeps receiver preferences as rank
matrices. `scripts/crosscheck.py` compares them.

## What is here

```
smprime/
  core.py        serial deferred acceptance from the definition: reachable
                 states, arcs, complete schedules, stable matchings,
                 invariants
  altcore.py     the second implementation; also handles incomplete lists
                 and unbalanced instances
  blocks.py      blocks, the block forest, the finest partition, and every
                 partition into blocks
  census.py      the exact census of prime instances (integer arithmetic)
  families.py    direct sums, the two cyclic families, random instances,
                 and the enumeration of all instances of a size
scripts/
  verify_paper.py    every checkable number of the paper, PASS or FAIL
  crosscheck.py      the two implementations, compared
  census_table.py    prints the census and writes data/census.csv
  size3_dataset.py   writes data/size3.csv.gz
  figure_products.py redraws the paper's figure from the definitions
tests/
  test_claims.py     the claims as assertions
data/
  size3.csv.gz       all 46,656 size-three instances with their invariants
  census.csv         the census to size eight
```

## Reproducing the paper

| claim | command | expected |
| --- | --- | --- |
| everything at once | `python scripts/verify_paper.py --all` | `0 checks failed` |
| Corollary 5.1, Boolean cubes at n = 3 | `verify_paper.py --all` | 10,368 |
| Table 3, decomposable at n = 3 | `verify_paper.py --all` | 888 |
| Theorem 6, uniqueness of the finest partition | `verify_paper.py --all` | checked against the meet of every partition into blocks |
| Theorem 9, the census | `python scripts/census_table.py` | Pi(4) = 109,986,835,968, decomposable 88,478,208 |
| Theorem 7 and Corollary 7.2, the six composition laws | `verify_paper.py` | 0 failures on random direct sums at sizes 4-6 |
| Proposition 12.3, the two families | `verify_paper.py` | same cube execution, stable sets 1 and n |
| the figure | `python scripts/figure_products.py` | `figures/fig_products.pdf` |
| the two implementations agree | `python scripts/crosscheck.py` | 0 disagreements on all 46,656 size-three instances |

The exhaustive pass takes about a minute; everything else is seconds.

## The size-three dataset

`data/size3.csv.gz` has one row for each of the 46,656 instances of size
three, 166 KB compressed. Columns: the two preference matrices `P` and `R`
flattened best-first, then `N` reachable states, `E` arcs, `Qstar` proposals
in total, `L` complete schedules, `kappa` the commutation index, `stab`
stable matchings, `shape` the block forest up to relabelling, `parts` the
sizes of the finest partition, `prime`, and `cube`.

```python
import gzip, csv, collections
with gzip.open("data/size3.csv.gz", "rt", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
collections.Counter(r["parts"] for r in rows)
# {'3': 45768, '2+1': 504, '1+1+1': 384}
collections.Counter(r["stab"] for r in rows)
# {'1': 34080, '2': 11484, '3': 1092}
```

Regenerate it with `python scripts/size3_dataset.py`, which takes a few
seconds and ends by checking that it wrote exactly 46,656 rows.

## Scope

Strict and complete preference lists on both sides, equal numbers of
proposers and receivers, and a serial scheduler that activates one unmatched
proposer at a time. `altcore` additionally handles incomplete lists and
unbalanced instances. Nothing here applies to ties, to synchronous updates,
to many-to-one markets or to matching with contracts, and no result should
be read as if it did.

Sizes: three is enumerable and is enumerated. Four is not - there are
110,075,314,176 instances - so size-four statements come from closed forms or
from certificates, never from a sweep. Anything obtained by search is
reported as a bound and labelled as one.

## Tests

```bash
python tests/test_claims.py            # standalone, no test runner needed
SMPRIME_FULL=1 python tests/test_claims.py   # adds the exhaustive sweep
```

The file uses plain functions and plain asserts, so `pytest` can collect it
as well.

## Citing

If this code is useful, cite the paper and, for the code itself, the archived
release. `CITATION.cff` carries both.

```
Ishida, Y. Prime factorisation of stable-matching instances: uniqueness,
simultaneous products, and an exact census. arXiv (2026).
```

Archived release: DOI to be inserted after the first Zenodo deposit.

## Licence

MIT. See `LICENSE`.
