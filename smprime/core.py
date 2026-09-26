"""
Serial deferred acceptance, built from the definition.

An instance is a pair (P, R) of tuples of tuples.  P[p] is proposer p's
strict complete ranking of the receivers and R[r] is receiver r's strict
complete ranking of the proposers, both given best first.  Sizes are equal;
incomplete lists are handled by the second implementation in `altcore`.

A state is (holder, ptr).  holder[r] is the proposer receiver r currently
holds, or -1, and ptr[p] is the number of proposals p has already made.  A
proposer is ACTIVE at a state when it is unheld and still has an unproposed
receiver.  A scheduler repeatedly picks an active proposer; the local update
sends that proposer's next proposal and lets the receiver keep the better of
its current holder and the newcomer.

Nothing here caches or approximates: every function recomputes from the
definition, so the module can be used to check other code.
"""
import itertools
import math

__all__ = ["reachable", "adjacency", "terminal_state", "complete_runs",
           "stable_matchings", "invariants", "is_cube"]


def _rank(R):
    return [{p: i for i, p in enumerate(row)} for row in R]


def _successors(P, rank, state):
    """(proposer, next state) for every proposer active at `state`"""
    holder, ptr = state
    n = len(P)
    held = {h for h in holder if h != -1}
    for p in range(n):
        if p in held or ptr[p] >= len(P[p]):
            continue
        r = P[p][ptr[p]]
        h = list(holder)
        q = list(ptr)
        q[p] += 1
        if h[r] == -1 or rank[r][p] < rank[r][h[r]]:
            h[r] = p
        yield p, (tuple(h), tuple(q))


def initial_state(P, R):
    return ((-1,) * len(R), (0,) * len(P))


def reachable(P, R):
    """every state reachable under every serial schedule.

    Returns (states, arcs, terminal).  `states` is a set, `arcs` counts the
    local updates available across all states, and `terminal` is the unique
    state with no active proposer.
    """
    rank = _rank(R)
    start = initial_state(P, R)
    seen, stack, arcs, terminal = {start}, [start], 0, None
    while stack:
        state = stack.pop()
        moved = False
        for _p, nxt in _successors(P, rank, state):
            moved = True
            arcs += 1
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
        if not moved:
            if terminal is not None and terminal != state:
                raise AssertionError("two terminal states: not possible for "
                                     "strict complete preferences")
            terminal = state
    return seen, arcs, terminal


def adjacency(P, R):
    """the reachable state graph keyed by pointer vector.

    By Lemma 1 of the paper a reachable state is determined by its pointer
    vector, so this is a faithful picture of the state graph and is the form
    the drawings use: {pointer vector: {proposer: successor pointer vector}}.
    """
    rank = _rank(R)
    out = {}
    for state in reachable(P, R)[0]:
        out[state[1]] = {p: nxt[1] for p, nxt in _successors(P, rank, state)}
    return out


def terminal_state(P, R):
    return reachable(P, R)[2]


def complete_runs(P, R):
    """the number of complete schedules, as paths of the state graph"""
    rank = _rank(R)
    memo = {}

    def paths(state):
        if state in memo:
            return memo[state]
        total, moved = 0, False
        for _p, nxt in _successors(P, rank, state):
            moved = True
            total += paths(nxt)
        memo[state] = 1 if not moved else total
        return memo[state]

    return paths(initial_state(P, R))


def stable_matchings(P, R):
    """every matching with no blocking pair, by definition.

    A matching is returned as a tuple m with m[p] the receiver of p.  This is
    a brute-force sweep over all n! matchings, which is what makes it a check
    on faster methods rather than a fast method itself.
    """
    n = len(P)
    prank = [{r: i for i, r in enumerate(row)} for row in P]
    rrank = _rank(R)
    out = []
    for m in itertools.permutations(range(n)):
        who = {r: p for p, r in enumerate(m)}
        if all(not (prank[p][r] < prank[p][m[p]]
                    and rrank[r][p] < rrank[r][who[r]])
               for p in range(n) for r in range(n)):
            out.append(m)
    return out


def is_cube(P, R):
    """does the run make exactly one proposal per proposer?"""
    return len(reachable(P, R)[0]) == 2 ** len(P)


def invariants(P, R):
    """the composable invariants of the paper, in one dictionary.

    N     reachable states
    E     arcs of the state graph
    Q     proposals made in total, the terminal pointer vector's sum
    L     complete schedules
    kappa L divided by the multinomial of the terminal pointer vector
    stab  stable matchings
    """
    states, arcs, term = reachable(P, R)
    q = term[1]
    Q = sum(q)
    L = complete_runs(P, R)
    multi = math.factorial(Q)
    for x in q:
        multi //= math.factorial(x)
    return dict(N=len(states), E=arcs, Q=Q, q=q, L=L, kappa=L / multi,
                stab=len(stable_matchings(P, R)))
