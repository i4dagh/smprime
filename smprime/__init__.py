"""
smprime - the prime structure of stable-matching instances.

Two independent implementations of serial deferred acceptance, the blocks
and the unique finest partition they generate, the exact census of prime
instances, and the families used to separate input structure from
behaviour.

    from smprime import core, blocks, census, families

    P, R = families.antiphase(4)
    core.invariants(P, R)          # N, E, Q, L, kappa, stable matchings
    blocks.finest_partition(P, R)  # the unique finest partition
    census.table(6)                # the exact census, Table 3 of the paper

The accompanying paper is

    Y. Ishida, Prime factorisation of stable-matching instances:
    uniqueness, simultaneous products, and an exact census.

Scope: strict and complete preference lists on both sides, equal numbers of
proposers and receivers, and a serial scheduler that activates one unmatched
proposer at a time.  `altcore` additionally handles incomplete lists and
unbalanced instances; nothing here applies to ties, synchronous updates,
many-to-one markets or matching with contracts.
"""
from . import core, blocks, census, families, altcore

__all__ = ["core", "blocks", "census", "families", "altcore"]
__version__ = "1.0.0"
