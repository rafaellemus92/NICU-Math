# experiments

Side explorations — not part of the app.

## `coupled_prime26_pangram.py`

Finds five pairs of primes that share one sum (Goldbach pairs), where the ten
primes' base-26 names together use every letter A–Z exactly once.

Plain base-26 names have no solution up to N = 18,250. With *coupled* digits
(each letter = its digit + the digit to its right, mod 26 — still reversible),
the smallest solution is N = 4296:

```
UKR + TEP  = 4296    (1187 + 3109)
 DB + NMF  = 4296    (53 + 4243)
 YL + AQV  = 4296    (349 + 3947)
 SH + CWZ  = 4296    (293 + 4003)
 IJ + OGX  = 4296    (659 + 3637)
```

Run (standard library only):

```
python3 experiments/coupled_prime26_pangram.py          # coupled, ~0.2s
python3 experiments/coupled_prime26_pangram.py --plain  # plain, no solution
```

Formal proofs of these facts (in Lean 4) live in [`wyrd/`](wyrd/).

[`checks/`](checks/) is a computer search, not a Lean proof, that enumerates
*every* solution instead of stopping at the first: exactly 12 five-pair pangrams
exist under the coupled naming (all with N ≤ 15990), and none at all under plain
naming, for every even N up to the 457000 cutoff beyond which the names are too
long to fit the alphabet.

Caveat: the coupling rule was chosen after the plain search failed, so the
result shows that *a* simple reversible naming yields a pangram, not that
primes "want" to spell the alphabet.
