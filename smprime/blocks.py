"""
Blocks, the finest partition, and the block forest.

A pair (A, B) with |A| = |B| = k is a BLOCK of the instance when the k
proposers in A rank exactly the k receivers in B in their first k places, and
the k receivers in B rank exactly the proposers in A in theirs.  The whole
instance is always a block.

The blocks of an instance form a laminar family (Proposition 9.5 of the
paper), so they arrange into a forest, and the paper's main theorem is that
the finest partition of the agents into blocks exists and is unique
(Theorem 6).  This module computes all of that from the definition.

An instance is INPUT-DECOMPOSABLE when that finest partition has more than
one part, and INPUT-PRIME otherwise.
"""
import itertools

__all__ = ["blocks", "finest_partition", "is_decomposable",
           "all_block_partitions", "meet", "block_forest", "forest_shape"]


def blocks(P, R):
    """every block, as a list of (frozenset A, frozenset B)"""
    n = len(P)
    out = []
    for k in range(1, n + 1):
        for A in itertools.combinations(range(n), k):
            B = set(P[A[0]][:k])
            if any(set(P[p][:k]) != B for p in A):
                continue
            if all(set(R[r][:k]) == set(A) for r in B):
                out.append((frozenset(A), frozenset(B)))
    return out


def _children(A, fam):
    """the maximal blocks properly inside A"""
    inner = [C for C in fam if C < A]
    return [C for C in inner if not any(C < D for D in inner)]


def finest_partition(P, R):
    """the finest partition of the proposers into blocks.

    Built downwards: a block splits exactly when the maximal blocks properly
    inside it cover it.  The result is a list of frozensets of proposers.
    """
    n = len(P)
    fam = {A for A, _B in blocks(P, R)}

    def split(A):
        kids = _children(A, fam)
        if len(kids) > 1 and sum(len(C) for C in kids) == len(A) \
                and set().union(*kids) == set(A):
            return [x for C in kids for x in split(C)]
        return [A]

    return sorted(split(frozenset(range(n))), key=sorted)


def is_decomposable(P, R):
    return len(finest_partition(P, R)) > 1


def all_block_partitions(P, R):
    """every partition of the proposers all of whose parts are blocks.

    Used to check Theorem 6 directly: the meet of all of these is the finest
    partition, and it is itself one of them.
    """
    n = len(P)
    parts = sorted({A for A, _B in blocks(P, R)},
                   key=lambda s: (-len(s), sorted(s)))
    out = []

    def rec(rest, acc):
        if not rest:
            out.append(list(acc))
            return
        first = min(rest)
        for A in parts:
            if first in A and A <= rest:
                rec(rest - A, acc + [A])

    rec(frozenset(range(n)), [])
    return out


def meet(p1, p2):
    """the common refinement of two partitions"""
    return sorted((A & B for A in p1 for B in p2 if A & B), key=sorted)


def block_forest(P, R):
    """the laminar family of blocks as a nested structure of proposer sets"""
    n = len(P)
    fam = {A for A, _B in blocks(P, R)}

    def node(A):
        return (A, [node(C) for C in sorted(_children(A, fam), key=sorted)])

    return node(frozenset(range(n)))


def forest_shape(P, R):
    """the block forest up to relabelling: a rooted tree of sizes.

    Written (k, (child shapes...)), so that "3(1 1)" is a three-block holding
    two singletons.
    """
    def shape(node):
        A, kids = node
        return (len(A), tuple(sorted(shape(k) for k in kids)))

    return shape(block_forest(P, R))


def show_shape(shape):
    k, kids = shape
    if not kids:
        return str(k)
    return "%d(%s)" % (k, " ".join(show_shape(c) for c in kids))
