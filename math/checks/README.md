# checks — complete enumeration of five-pair prime pangrams (2026-10-16)

Two independent enumerators that list **every** five-pair prime pangram for
each even sum, instead of stopping at the first one as
[`../coupled_prime26_pangram.py`](../coupled_prime26_pangram.py) does. They reuse that
script's encoding and primality code (`enumerate_all.py` imports it; `pangram_all.c`
re-implements the naming rule and a sieve).

```sh
python3 enumerate_all.py ../coupled_prime26_pangram.py coupled 1352 20000 15
gcc -O2 -o pangram_all pangram_all.c
./pangram_all coupled 1352 457000 > coupled_all.txt     # ~2 min
./pangram_all plain   1352 457000 > plain_all.txt       # ~2 min
```

Both agree on the range 1352–20000 (12 solutions at 11 sums).

## Why 457000 is enough

A name has as many letters as the number has base-26 digits, under either naming
rule. If N ≥ 457001 then in every pair (p, q) with p < q: p ≤ 25 gives q ≥ 456976 = 26⁴
(5 letters), 26 ≤ p ≤ 675 gives q ≥ 456326 (≥ 4 letters), 676 ≤ p ≤ 17575 gives
q ≥ 439426 (≥ 4 letters), and p ≥ 17576 gives 4 + 4. So every pair has at least
6 letters and five pairs have at least 30 > 26.

The search also skips odd N, the prime 2, and N < 1352. For the coupled rule these
exclusions are Lean theorems: `sum_even` and `two_not_mem` in
[`../wyrd/Wyrd/Parity.lean`](../wyrd/Wyrd/Parity.lean), and `lower_bound` in
[`../wyrd/Wyrd/Pangram.lean`](../wyrd/Wyrd/Pangram.lean). Their proofs use only
that a positive number's name is non-empty and has as many letters as the number
has base-26 digits, which holds for the plain rule too, so the same arguments
carry over on paper. They are not formalised for the plain rule.

## Results

* **Coupled naming:** exactly **12** five-pair prime pangrams exist in total, at
  11 distinct sums (`coupled_all.txt`): 4296, 6942, 8242, 8970, 9216, 12510,
  12516, 13812 (two solutions), 14634, 15726, 15990. So 4296 is the smallest
  sum, it is the only solution at that sum, and its largest prime 4243 is the
  smallest maximum prime of any solution.
* **Plain naming:** **no** five-pair prime pangram exists at any sum
  (`plain_all.txt` is empty). This extends the "no solution up to N = 18,250" in
  [`../README.md`](../README.md) to a complete answer.

## What is and is not machine-checked

That 4296 is the smallest sum is already proved in Lean (`smallest_pangram_sum` in
[`../wyrd/Wyrd/Smallest.lean`](../wyrd/Wyrd/Smallest.lean)), and this enumeration
agrees with it. Everything else here is a computer search with an informal
soundness argument, not a Lean proof: the complete list of 12 solutions, the
457000 cutoff, and the plain-rule result, which the roadmap item "Plain base-26
has no pangram up to 18,250" in [`../wyrd/ROADMAP.md`](../wyrd/ROADMAP.md) still
lists as open.
