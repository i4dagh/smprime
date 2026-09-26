"""
Instances to build things out of, and the two families the paper separates.

`direct_sum` glues instances into one, which is how the products theorem is
tested; `aligned` and `antiphase` are the two cyclic families that share the
identical Boolean-cube execution while sitting at opposite ends of
everything that execution cannot see (Proposition 12.3).

    aligned(n)     p_i and r_i rank each other first, then both rotate.
                   Maximally decomposable: n singleton blocks, one stable
                   matching.
    antiphase(n)   the same rotation on the proposer side, shifted by one on
                   the receiver side, so no pair is mutually first. Prime,
                   with n stable matchings.
"""
import itertools
import random

__all__ = ["direct_sum", "aligned", "antiphase", "random_instance",
           "all_instances", "figure_instance"]


def direct_sum(parts):
    """one instance whose blocks are the given instances, side by side.

    Each agent ranks its own block first, in the block's own order, and
    everything outside afterwards; that is exactly the block condition.
    """
    sizes = [len(p) for p, _r in parts]
    n = sum(sizes)
    P, R, off = [], [], 0
    for (Pi_, Ri_), k in zip(parts, sizes):
        outside = [x for x in range(n) if not (off <= x < off + k)]
        for row in Pi_:
            P.append(tuple([x + off for x in row] + outside))
        for row in Ri_:
            R.append(tuple([x + off for x in row] + outside))
        off += k
    return tuple(P), tuple(R)


def aligned(n):
    P = tuple(tuple((i + j) % n for j in range(n)) for i in range(n))
    R = tuple(tuple((i - j) % n for j in range(n)) for i in range(n))
    return P, R


def antiphase(n):
    P = tuple(tuple((i + j) % n for j in range(n)) for i in range(n))
    R = tuple(tuple((i + 1 + j) % n for j in range(n)) for i in range(n))
    return P, R


def random_instance(rng, n):
    if isinstance(rng, int):
        rng = random.Random(rng)
    return (tuple(tuple(rng.sample(range(n), n)) for _ in range(n)),
            tuple(tuple(rng.sample(range(n), n)) for _ in range(n)))


def all_instances(n):
    """every instance of size n, as a generator.

    There are (n!)^(2n) of them: 16 at n = 2, 46,656 at n = 3, and
    110,075,314,176 at n = 4, so only the first two sizes are enumerable.
    """
    orders = list(itertools.permutations(range(n)))
    for P in itertools.product(orders, repeat=n):
        for R in itertools.product(orders, repeat=n):
            yield P, R


# the instance drawn in Fig 1 of the paper: a size-three prime factor with
# two stable matchings, glued to the opposed size-two instance
FIG_FACTORS = (((( 0, 1, 2), (0, 1, 2), (2, 0, 1)),
                ((2, 0, 1), (0, 1, 2), (0, 1, 2))),
               (((0, 1), (1, 0)),
                ((1, 0), (0, 1))))


def figure_instance():
    """(the two factors, their direct sum)"""
    return FIG_FACTORS, direct_sum(list(FIG_FACTORS))
