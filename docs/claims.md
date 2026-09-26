# What each statement rests on

Every numbered statement in the paper carries a status tag. This table
repeats those tags and says, where code is involved, which command in this
repository checks the statement. It was generated from the paper source, so
the tags are the paper's own and not a paraphrase.

The tags mean

* **PROVED** a proof is given in the paper or cited from the literature.
* **EXHAUSTIVE** checked on every instance of the size named; at size three
  that is all 46,656 instances with strict complete preferences.
* **EXACT** a finite candidate set was fixed in advance by a proved
  statement, and every candidate in it was settled. This is how sizes four
  to six are reached, where enumerating instances is impossible.
* **TARGETED** a particular instance was constructed or searched for, and is
  supplied as a certificate.

A tag never promotes a computation to a proof. Where a statement holds at
every size the tag says PROVED; where it was verified only at certain sizes,
the tag names them.

| statement | what it says | status in the paper | checked here by |
| --- | --- | --- | --- |
| Lemma 1 | states are determined by proposal counts | PROVED | `tests/test_claims.py::test_lemma1_state_is_its_pointer_vector` |
| Theorem 2 | local commutativity | PROVED | - |
| Lemma 3 | persistent enablement | PROVED | - |
| Theorem 4 | antimatroid and exchange | PROVED | - |
| Theorem 5 | Boolean-cube characterisation | PROVED | `tests/test_claims.py::test_theorem5_cube_iff_distinct_first_choices`, and exhaustively by `scripts/verify_paper.py --all` |
| Theorem 6 | uniqueness of the finest input partition | PROVED | `tests/test_claims.py::test_theorem6_finest_partition_is_the_meet`, against the meet of every partition into blocks |
| Theorem 9.4 | blocks are the square components of the filtration | PROVED; EXHAUSTIVE at n = 3, verified at n = 4 | - |
| Proposition 9.5 | the blocks form a forest | PROVED | implied by `blocks.block_forest`, which would raise if the family were not laminar |
| Theorem 9.6 | primality is a covering failure | PROVED; EXHAUSTIVE | - |
| Proposition 9.7 | the exact-cover polynomial, and why it factorises | PROVED; EXHAUSTIVE at n = 3; TARGETED at n = 4 to 6 | - |
| Theorem 7 | products | PROVED | `tests/test_claims.py::test_theorem7_products_and_composition_laws` |
| Lemma 7.1 | a direct sum never splits a proposer | PROVED; the component description EXHAUSTIVE at n = 3 | - |
| Corollary 7.2 | how each invariant composes, and why it matters which | PROVED; EXHAUSTIVE at n = 3; EXACT at n = 4 to 6 | same test: all six laws on random direct sums at sizes four to six |
| Theorem 8 | the converse fails | PROVED | - |
| Theorem 6.1 | the behavioural factorisation is unique too | PROVED; EXHAUSTIVE | - |
| Proposition 9.10 | the dynamic decomposition structure is flat, and its counting degenerates | PROVED; EXHAUSTIVE at n = 3; EXACT at n = 4 to 6 | - |
| Theorem 12 | regular symmetry forces the Boolean cube | PROVED | - |
| Corollary 12.1 | the regular anti-phase templates run as a Boolean cube | PROVED; EXHAUSTIVE for orders at most 5 | - |
| Proposition 12.2 | execution structure and the stable set are independent invariants | PROVED, with certificates; EXHAUSTIVE at n = 3 | - |
| Proposition 12.3 | two Latin families that the execution cannot tell apart | PROVED; EXHAUSTIVE for n at most 6 | `tests/test_claims.py::test_proposition12_3_two_families`, sizes two to six |
| Theorem 9 | exact census of input-prime instances | PROVED; EXACT | `scripts/census_table.py`, and `tests/test_claims.py::test_theorem9_census_matches_table3` |
| Corollary 13 | census for prime size | PROVED; EXACT | - |
| Proposition 21 | a block is tight and regular, and tightness alone is not enough | PROVED; EXHAUSTIVE at n = 3 | - |
| Theorem 21.1 | the partition recursion | PROVED | - |
| Proposition 21.4 | how large the state count of an indecomposable instance must be | PROVED; EXHAUSTIVE at n = 2 and 3 | - |

Statements with a dash in the last column are proofs on paper with no
computational content, or computations that belong to the companion
classification paper rather than to this repository.

Two implementations, not one: every exhaustive count was produced twice, by
`smprime.core` and by `smprime.altcore`, which share no code.
`scripts/crosscheck.py` runs the comparison and reports zero disagreements
over all 46,656 size-three instances and over samples at sizes four and
five.

