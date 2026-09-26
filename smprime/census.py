"""
The exact census of input-prime instances (Theorem 9 of the paper).

Write T(n) = (n!)^(2n) for the number of balanced strict complete instances
of size n and Pi(n) for the number of input-prime ones.  Because the finest
partition is unique, the instances are partitioned by its shape, and

    T(n) = sum over partitions lambda of n of
               N_lambda(n) * product over parts k of Pi(k) * ((n-k)!)^(2k),

    N_lambda(n) = (n! / product k_i!)^2 / product over sizes of m_j!,

where m_j counts the parts of size j.  The one-part term is Pi(n), so the
identity determines Pi recursively.

Everything here is exact integer arithmetic.
"""
import math

__all__ = ["partitions", "census", "table", "decomposable_fraction"]


def partitions(n, cap=None):
    """the partitions of n as non-increasing lists"""
    cap = n if cap is None else cap
    if n == 0:
        yield []
        return
    for k in range(min(n, cap), 0, -1):
        for rest in partitions(n - k, k):
            yield [k] + rest


def census(nmax):
    """Pi(n) for n up to nmax, plus the per-shape decomposable counts.

    Returns (Pi, rows) where rows[n] = (T(n), decomposable, Pi(n), shapes)
    and shapes maps a partition of n with at least two parts to the number of
    instances whose finest partition has that shape.
    """
    Pi = {1: 1}
    rows = {1: (1, 0, 1, {})}
    for n in range(2, nmax + 1):
        T = math.factorial(n) ** (2 * n)
        shapes, total = {}, 0
        for lam in partitions(n):
            if len(lam) == 1:
                continue
            mult = {}
            for k in lam:
                mult[k] = mult.get(k, 0) + 1
            N = (math.factorial(n)
                 // math.prod(math.factorial(k) for k in lam)) ** 2
            for m in mult.values():
                N //= math.factorial(m)
            term = N
            for k in lam:
                term *= Pi[k] * math.factorial(n - k) ** (2 * k)
            shapes[tuple(lam)] = term
            total += term
        Pi[n] = T - total
        rows[n] = (T, total, Pi[n], shapes)
    return Pi, rows


def decomposable_fraction(n, rows=None):
    """the share of instances that decompose, as a float"""
    if rows is None:
        rows = census(n)[1]
    T, dec, _Pi, _shapes = rows[n]
    return dec / T


def table(nmax=8):
    """the rows of Table 3 as dictionaries, ready to print or to write out"""
    _Pi, rows = census(nmax)
    out = []
    for n in range(1, nmax + 1):
        T, dec, Pi_n, shapes = rows[n]
        out.append(dict(n=n, T=T, decomposable=dec, prime=Pi_n,
                        fraction=(dec / T if T else 0.0),
                        shapes={"+".join(map(str, k)): v
                                for k, v in sorted(shapes.items())}))
    return out
