# Prime-26 pangram project — session archive (2026-10-16)

Everything produced in this Claude session on the "Prime-26" language: primes named by their base-26
digits (A=0 … Z=25), and perfect pangrams built from ten such names.

**What is here:** C and Python sources, raw run logs, machine-readable results, a test script, a Makefile.
**What is not here:** this session contains no Lean, JavaScript or Lake files, no onset/coda data and no
dictionaries — nothing of that kind was created or uploaded in this conversation, so it could not be
packaged. If those belong to your own repository (the coupled-naming project), they will have to be
packaged from there.

## Results in one screen

1. The 5-vs-5 equation pangram `YR BQL CWH DNF GAX = KV MT OP ESJ IUZ` (10,125 = 10,125) verifies: all ten
   values prime, every letter once. Mod-25 theorem (casting out 25s): the sum of any Prime-26 perfect
   pangram is ≡ 0 (mod 25); for an *equation* pangram each side is ≡ 0 on its own (here 150 and 175 are
   the two sides' letter-sums, and 10,125 = 25·405).
2. **Equal-sum five-pair pangrams (five pairs p+q = N, all 26 letters once): none exist.** Proof bounds
   N < 2·26³ = 35,152 and words to ≤ 4 letters; exhaustive search of every even N < 40,000 finds nothing
   (two independent implementations). Best partials reach four pairs (20 letters).
3. **Equal-difference five-pair pangrams (q − p = D): exactly three** in all of Prime-26 —
   D = 204, 258, 534 (proof bounds: D even, 28 ≤ D < 17,576, words ≤ 4 letters; exhaustive search).
   Derived constraint: letter-sum of the five smaller words ≡ 10·D (mod 25).
   The factor 6 in all three D is a supply effect (Hardy–Littlewood): prime pairs p, p+D are twice as
   common when 3 | D (mean candidates 1,555 vs 778 over all D in range; 5 | D adds ≈25% more).
4. **Counting all 5-vs-5 equation pangrams.** Exact number of perfect pangrams (10 prime words, each
   letter once) by DP over the 2²⁶ letter subsets, verified against brute force on sub-instances:

   | max word length | perfect pangrams (exact)        | balanced-split fraction (uniform sampling) | equation pangrams (estimate) |
   |-----------------|---------------------------------|---------------------------------------------|------------------------------|
   | ≤ 3 letters     | 2,476,752,460,975               | 4.03e-3 ± 0.06e-3 (4,007 hits / 1e6)        | 9.98e9 ± 0.16e9              |
   | ≤ 4 letters     | 1,820,178,519,744,870           | 1.03e-4 ± 0.07e-4 (205 hits / 2e6)          | 1.9e11 ± 0.13e11             |
   | ≤ 5 letters     | 17,712,554,714,431,732          | 1.4e-5 ± 0.4e-5 (14 hits / 1e6)             | 2.5e11 ± 0.7e11              |
   | ≤ 6 letters     | see results/results.json        | see results/results.json                    | see results/results.json     |

   Words of 8+ letters cannot occur in an equation pangram; 7-letter words only in a few profiles with
   ≥ 6 single-letter words (negligible, ~10⁷–10⁸). Brute-force enumeration runs at ≈ 9.4e5 pangrams/s
   (one core): ≈ 60 years for the ≤ 4-letter universe alone. Headline: on the order of 2 × 10¹¹
   equation pangrams — an earlier off-hand estimate of 10¹⁵ was wrong by ~4 orders of magnitude.

## Layout (original directory structure preserved)

```
tmp/prime26.py            first script: verifies the equation pangram, then a (slow, Python) five-pair search
scratchpad/pairs.c        exhaustive equal-sum five-pair search over even N < Nmax (default 2·26⁴), words < 26⁴
scratchpad/pairs_test.c   same with -DTESTMODE=1: odd numbers instead of primes (sanity test of the exact cover)
scratchpad/diff.c         exhaustive equal-difference search over even D ≤ Dmax; prints solutions + 10D mod 25 check
scratchpad/pack.c         per-D statistics: candidate pairs, two-letter pairs, largest disjoint packing
scratchpad/pang.c         Knuth-style sequential importance sampler (superseded: huge variance; kept for the record)
scratchpad/pangdp.c       exact DP count of perfect pangrams with words ≤ K letters + uniform sampling from the DP
scratchpad/brute.c        independent brute-force partition counter used to validate pangdp (sub-instances)
scratchpad/enumfull.c     time-limited brute-force enumeration of pangrams (throughput measurement)
scratchpad/*.out, *.err   raw logs of the runs (dp4 = K≤4, dp5 = K≤5, dp6 = K≤6, pack.out = pack.c output)
results/results.json      all numbers above, machine-readable
results/pack_by_D.tsv     D, candidate pairs, two-letter pairs, max disjoint pairs — for every even D in [28, 17574]
results/logs/             copies of the run logs (dp3.out was captured from the console)
tests/test_solutions.py   pure-Python checks: pangram, the three solutions, the mod-25 identities, near-miss;
                          --slow re-derives the DP validation counts with a third, independent implementation
Makefile                  builds everything; `make check` runs the quick end-to-end checks
```

## Build and run

```
make                       # gcc, no dependencies
./pairs 40000              # equal-sum search: 0 solutions, ~0.2 s
./diff 20000               # equal-difference search: D = 204, 258, 534; ~20 s
./pack > pack.out          # per-D supply statistics; ~2.5 min
./pangdp K NSAMPLES SEED [LETTERS:j ...]
                           # exact count for words ≤ K letters, then NSAMPLES uniform samples;
                           # optional LETTERS:j prints dp[letter set][j words] for comparison with ./brute
                           # memory: 2²⁶·window·8 bytes ≈ 2.1 GB (K=4), 2.7 GB (K=5), 3.2 GB (K=6) + a sieve to 26^K
                           # time (one core): K=3 1 min, K=4 6 min, K=5 23 min, K=6 ~1 h, plus sampling (~1 ms/sample at K=5)
./brute K LETTERS:j ...    # independent partition counts, e.g. ./brute 4 ABCDEFGHIJKL:5  -> 27152
./enumfull 4 90            # brute-force throughput for 90 s
python3 tests/test_solutions.py [--slow]
```

Word tables are generated internally from a sieve (no dictionary needed): every prime below 26^K whose
base-26 digits are pairwise distinct is a word. No secrets, caches or build outputs are included.
