# prime-pangram — preserved search code, data and results (2026-10-16)

Permanent home for every result-producing file of the prime-pangram work that
previously existed only in session archives, `/tmp` or a scratchpad. Nothing
here is part of the sgrounds app. Every number below is marked either
**reproduced** (re-run in this checkout on 2026-10-16, timings measured here) or
**archived** (copied verbatim from the archived logs; not re-run here).

## Contents and provenance

| Path | Origin | What it holds |
|---|---|---|
| `search/` | `prime26-pangram-v1.zip`, the archive of the Prime-26 session of 2026-10-16. Its directory structure is kept as-is, including the original `tmp/` and `scratchpad/` sub-folders, so its `Makefile` and `README.md` work unchanged. | Five-pair searches (equal sum, equal difference), exact DP counts of perfect pangrams, importance sampling, brute-force validators, raw run logs, `results/results.json`, `results/pack_by_D.tsv`, tests, Makefile. |
| `nicu-pangram/` | `pangram-project.zip` → `NICU-Module/pangram/`, i.e. repository `rafaellemus92/NICU-Module`, branch `claude/pangram-prime-words-kgdssi`, commit `2323373`, copied file-for-file. | Prime perfect pangrams in bijective base 26 under a pronounceability rule: the exact onset/coda lists (`clusters.py`), the generated dictionaries (`results/english_prime_words.txt`, `results/free_prime_masks.txt`), Python + C search and counting code, JSON results and lattice logs. |
| `MANIFEST-upstream-2026-10-16.md` | `pangram-project.zip` | That archive's own manifest: which files came from which repository, branch and commit. |
| `logs/` | this session | Complete console output of every command run here on 2026-10-16: elan install, `lake update` / `lake exe cache get` / `lake build` / audit, and the `search/` and `nicu-pangram/` check runs with their timings. |
| `../coupled_prime26_pangram.py`, `../checks/`, `../wyrd/`, `../wyrd-mathlib/` | Already on this branch. | Coupled base-26 five-pair finder, the complete enumerations, the Lean 4 proofs. The copy of these inside `pangram-project.zip` is byte-identical to this branch at commit `633f161`, so it was not duplicated here. |

**Not found anywhere:** files named `verify.js`, `verify2.js` or `roots.js`.
Neither archive contains them, this container's `/tmp` and scratchpad were empty
when the session started, and the upstream manifest records that neither
repository contains any JavaScript for this project. If they exist on another
machine they still have to be added by hand.

## Three different numerations — read this before comparing numbers

The three code bases answer different questions under different definitions.
None of the counts are comparable across rows.

| Code | Letters → number | "Word" | Problem |
|---|---|---|---|
| `search/` ("Prime-26") | Plain base 26, A=0 … Z=25, no leading A (a numeral has no leading zero). `YR` = 24·26 + 17 = 641. | A prime whose base-26 digits are pairwise distinct. No dictionary: the word table is generated from a sieve. | Perfect pangrams of ten words (26 letters once); equation pangrams (two groups of five with equal sums); five pairs with a common sum or a common difference. |
| `nicu-pangram/` | Bijective base 26, A=1 … Z=26. `AB` = 1·26 + 2 = 28. | A prime that is pronounceable: onset + nucleus + coda, nucleus = one vowel or an ordered pair of distinct vowels (vowels a e i o u y), onset ∈ ONSETS (70, incl. empty), coda ∈ CODAS (175, incl. empty), from `clusters.py`. Primality: deterministic Miller–Rabin, 12 bases (`mr.c`), re-checked in pure Python. | Perfect pangrams (≤ 6 words), exact counts by subset DP / inclusion–exclusion, and the lattice of relaxations R(o,c), F(n,m) of the cluster lists. |
| `../coupled_prime26_pangram.py`, `../checks/`, `../wyrd/` | Plain base 26 (A=0 … Z=25) **or** the *coupled* naming: each letter = its digit + the digit to its right, mod 26 (reversible). | Any prime. | Five Goldbach pairs p+q = N whose ten names use all 26 letters once. Coupled: smallest N = 4296 (Lean-proved), exactly 12 solutions in all (computer search). Plain: none exist (computer search). |

## `search/` — Prime-26 (plain base 26, distinct-digit primes)

Build: `cd search && make` (gcc, no dependencies; warnings about `calloc` are
harmless). Memory: `pangdp` needs 2²⁶·window·8 bytes ≈ 2.1 GB (K=4), 2.7 GB
(K=5), 3.2 GB (K=6) plus a sieve to 26^K.

| Experiment | Command | Definition | Result | Runtime | Status |
|---|---|---|---|---|---|
| Equation pangram check | `python3 tmp/prime26.py` (NumPy) or `python3 tests/test_solutions.py` | `YR BQL CWH DNF GAX = KV MT OP ESJ IUZ`: ten distinct-digit primes, 26 letters once, both sides sum to 10,125. Mod-25 theorem: 26 ≡ 1 (mod 25), so a perfect pangram's sum ≡ Σ(0..25) ≡ 0 (mod 25); each side of an equation pangram is ≡ 0 on its own. | verified; sides 150 and 175 as letter sums, 10,125 = 25·405 | 0.03 s (tests) | reproduced |
| Equal-sum five pairs | `./pairs 40000` | Five pairs (p,q) of words with p+q = N for all five, every letter once. Proved bounds: N even, N < 2·26³ = 35,152, words ≤ 4 letters. Exact cover over all even N < 40,000. | **0 solutions**; no 4-pair cover of all 26 letters either; best partial = 4 pairs at N = 10,146 leaving C M Q R U Y | 0.2 s | reproduced |
| Equal-sum, sanity variant | `./pairs_test 40000` | Same program with `-DTESTMODE=1`: odd numbers instead of primes, to exercise the exact cover. | (sanity only) | ≈ 0.2 s | archived |
| Equal-difference five pairs | `./diff 20000` | Five pairs with q − p = D, every letter once. Proved bounds: D even, 26 ∤ D, 28 ≤ D < 26³ = 17,576, words ≤ 4 letters. Exhaustive over even D ≤ 20,000. Derived identity: letter-sum of the five smaller words ≡ 10·D (mod 25). | **exactly three: D = 204, 258, 534** (solutions in `results/results.json`) | 26.3 s here (archive: ~20 s) | reproduced |
| Supply statistics per D | `./pack > pack.out` | For every even D in [28, 17574]: candidate prime pairs, two-letter pairs, size of the largest letter-disjoint packing. | `results/pack_by_D.tsv`; mean candidates 1,554.8 when 3 \| D vs 777.5 otherwise; 5 \| D adds ≈ 25 % | ≈ 2.5 min | archived |
| Exact count of perfect pangrams | `./pangdp K NSAMPLES SEED` | DP over the 2²⁶ letter subsets with an exact word counter; words ≤ K letters. Then NSAMPLES uniform samples from the DP, counting pangrams that admit a balanced 5-vs-5 split. | K=3: 2,476,752,460,975; K=4: 1,820,178,519,744,870; K=5: 17,712,554,714,431,732; **K=6: not finished** | K=3: 60 s + 23 s sampling (archive `dp3.out`); K=4: ≈ 6 min; K=5: ≈ 23 min; K=6: ran to 75 % at 2,802 s and did not finish (`scratchpad/dp6.err`, `dp6.out` empty) | archived; K=3 **reproduced** here with `./pangdp 3 1000000 23`: same count and same 4,007 balanced hits, 94 s + 54 s sampling while sharing the CPU with the Lean build (`results/logs/dp3_rerun.out`) |
| Validation of the DP | `./brute 4 ABCDEFGHIJKL:5 ABCDEFGHIJKL:4 ABCDEFGHIJKL:3 ABCDEFGHIJKLM:5` and `python3 tests/test_solutions.py --slow` | Independent brute-force partition counts on sub-instances (letter subset, fixed word count), compared with `dp[subset][j]` printed by `pangdp ... LETTERS:j`. | 27152, 73155, 30128, 122443 (all three implementations agree; full table in `results/results.json` → `validation_checks`) | brute: 0.7 s; `--slow`: 40.5 s | reproduced |
| Equation-pangram estimates | sampling phase of `./pangdp` | Fraction of uniform random perfect pangrams with a balanced split, times the exact count. | K≤3: 9.98e9 ± 0.16e9; K≤4: 1.9e11 ± 0.13e11; K≤5: 2.5e11 ± 0.7e11. Headline: ≈ 2 × 10¹¹ equation pangrams (an earlier guess of 10¹⁵ was wrong by ≈ 4 orders of magnitude). 8+-letter words cannot occur; 7-letter words contribute an estimated 10⁷–10⁸. | included in the `pangdp` runs | archived (Monte-Carlo estimates with standard errors, not exact) |
| Brute-force throughput | `./enumfull 4 90` | Time-limited enumeration of all pangrams with words ≤ 4 letters. | 84,410,368 pangrams in 90.1 s ≈ 9.4e5/s; ≈ 61.7 core-years for the whole K≤4 universe | 90 s | archived |
| Importance sampler (superseded) | `./pang` | Knuth-style sequential importance sampling; kept for the record, huge variance. | superseded by `pangdp` | — | archived |

Logs: `results/logs/*.out` are copies of `scratchpad/*.out` (byte-identical;
`dp3.out` was captured from the console). `scratchpad/*.err` hold the progress
lines of each DP run.

## `nicu-pangram/` — pronounceable primes in bijective base 26

Build: `cd nicu-pangram && gcc -O2 -shared -fPIC -o libmr.so mr.c && gcc -O2 -o xcover xcover.c && gcc -O2 -o freedp freedp.c`.
Requires Python 3 with NumPy. Full reproduction recipe, with per-script
timings, is in `nicu-pangram/README.md` ("Reproduce everything": ≈ 2–3 h on
4 cores, 8 GB RAM).

| Experiment | Command | Definition | Result | Runtime | Status |
|---|---|---|---|---|---|
| Self-tests | `python3 core.py && python3 engine.py` | Numeration check values (XWOZC = 11,382,491 …); the counting engine with primality off must equal the closed form N₀ = 20!·[x²⁰](1+x+x²)¹² = 2,970,573,351,983,677,440,000. | ok; match = True; float engine rel. err 3.0e-8 | 0.4 s + 66 s | reproduced |
| (a) English lists | `python3 run_a_english.py` | Dictionary = all pronounceable distinct-letter prime words under `clusters.py`; exact-cover search (`xcover.c`) for perfect pangrams. | 289,404 pronounceable words, **16,243 prime**, 1,633,290 search nodes, **0 perfect pangrams**. Regenerates `results/english_prime_words.txt` and `results/a_english.json` (byte-identical to the archived copies). | 7.3 s | reproduced |
| Packing bound | `python3 structure.py` | A prime word of ≥ 2 letters ends in a letter coprime to 26, so every non-empty coda is an "odd coda" (ends in c g k q s w). Subset DP: ≤ 6 onsets + ≤ 6 odd codas cover at most 17 of the 20 consonants, so result (a) holds regardless of which numbers are prime. | max 17 consonants (English); 20 once any 2-consonant onset or coda is allowed | 2 min 21 s | reproduced |
| (d) Free CC·V·CC count | `python3 run_d_free_count.py && ./freedp results/free_prime_masks.txt` | Onset ≤ 2 consonants, one vowel, coda ≤ 2 consonants; exact count of unordered 6-word perfect pangrams by inclusion–exclusion mod three 31-bit primes + CRT; `freedp.c` is an independent 64-bit DP. | 34,587 prime words; **11,261,264,735,669** (both implementations) | 42 s | archived |
| (c) First moments | `python3 run_c_english.py`, `python3 check_coprime.py` | E = Σ over pangrams of Π P(word prime), with naive 1/ln n and refined (13/6)/ln n on coprime last letters. | English: E_naive 7.06e4, E_refined exactly 0; free: 1.108e13 vs observed 1.126e13 | — | archived |
| (b.1) Smallest single added cluster | `for i in 0 1 2; do python3 reach.py $i; done; python3 run_b_single.py 5` | One foreign cluster of k consonants plus English prime words elsewhere. | k=1,2: 0; k=3: 100 working clusters (all codas ending in q), 946,514 solutions; k=4: 15,022 / 92,916,257; k=5: 558,205 / 4,128,113,285 (`results/b_single_cluster.json`, `results/b_single_k5.txt`) | k=4 ≈ 1 min, k=5 ≈ 35 min | archived |
| (b.2) Lattice of regimes | `python3 run_b_lattice.py B`, `python3 run_b_lattice.py "R(0,0)" … "R(2,2)"`, `python3 run_b_lattice.py "R(3,0)" "R(0,3)" --nowitness`, `python3 summarize.py` | R(o,c) = English lists plus all consonant strings of length ≤ o as onsets and ≤ c as codas; F(n,m) = free family (onset ≤ n, one vowel, coda ≤ m). Exact counts, minimum number of non-English clusters, witnesses. | `results/b_lattice/*.json`, tables in `nicu-pangram/README.md` | most of the ≈ 3 h | archived |
| Spot checks | `python3 check_single.py jvq; python3 check_onset3.py 3; python3 check_onset3.py 4; python3 check_coprime.py` | Exact-cover enumeration of all pangrams whose only foreign cluster is coda `jvq` (38,093, matching the reach tables); no 3-consonant onset works; 4-consonant onsets do. | as stated | — | archived |

The onset/coda data are the two Python lists `ONSETS` (70 entries) and
`CODAS` (175 entries) in `nicu-pangram/clusters.py`, each entry paired with an
example word; both lists contain the empty cluster. Conventions (y is a vowel,
`qu` = onset `q` + vowel, no coda ends in q, no doubled letters) are documented
at the top of that file.

Dictionaries: `results/english_prime_words.txt` (16,243 words, one per line, regenerated by
`run_a_english.py`) and `results/free_prime_masks.txt` (34,587 mask/count
lines for the free regime, regenerated by `run_d_free_count.py`). Both are
checked in; nothing has to be downloaded.

## `../wyrd/` — Lean 4 proofs (core Lean, no Mathlib)

Branch `claude/new-session-sbrl43`, commit `633f161`; the Lean sources were not
modified in this session. Project `experiments/wyrd/`: `lakefile.toml` (one
library, `Wyrd`, no dependencies), `lake-manifest.json` (no packages),
`lean-toolchain` = `leanprover/lean4:v4.35.0`. Modules: `Wyrd.lean`,
`Wyrd/Encoding.lean`, `Wyrd/Pangram.lean`, `Wyrd/Distinct.lean`,
`Wyrd/Parity.lean`, `Wyrd/Minimal.lean`, `Wyrd/MinimalData.lean`,
`Wyrd/MinimalTable0.lean` … `MinimalTable3.lean`, `Wyrd/Smallest.lean`,
`Wyrd/Euclid.lean`, `Wyrd/Sqrt2.lean`, plus `Audit.lean` and `scripts/`.

Commands run on 2026-10-16 with elan 4.2.4, Lean 4.35.0, Lake 5.0.0 (complete
output in `logs/lean-build-2026-10-16.log`):

| Command | Result | Time |
|---|---|---|
| `lake update` | `toolchain not updated; already up-to-date`, exit 0 (no dependencies to update) | 0.1 s |
| `lake exe cache get` | `error: unknown executable cache`, exit 1. Expected: the `cache` executable comes from Mathlib, and `wyrd` has no dependencies, so there is nothing to fetch. Only `../wyrd-mathlib/` has that executable. Nothing was changed to work around it. | 0.1 s |
| `lake build` | `Build completed successfully (16 jobs)`, exit 0 | 17 min 01 s wall, 28 min 23 s user, on 4 cores. `MinimalTable0..3`: 277 s, 452 s, 627 s, 972 s; `Minimal` 28 s; `Pangram` 12 s; `Smallest` 4 s; everything else under 2 s |
| `lake env lean Audit.lean` | All 14 audited theorems depend only on `propext`, `Classical.choice`, `Quot.sound` (`solution_names` on none). No `sorryAx`, no `Lean.ofReduceBool`, so no proof is unfinished and none trusts compiled code. | 0.5 s |

Audited theorems: `decode_encode`, `encode_injective`, `solution_names`,
`solution_isPangram`, `lower_bound`, `primes_nodup`, `length_primesOf`,
`sum_even`, `two_not_mem`, `no_smaller_pangram`, `smallest_pangram_sum`,
`exists_prime_gt`, `primes_infinite`, `no_fraction_squares_to_two`.

Reproduce:

```sh
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain none
export PATH=$HOME/.elan/bin:$PATH
cd experiments/wyrd           # elan installs leanprover/lean4:v4.35.0 from lean-toolchain on first use
lake update                   # no-op, no dependencies
lake build                    # ~17 min on 4 cores
lake env lean Audit.lean      # must show no sorryAx / ofReduceBool
```

## Software versions used for the reproduced runs

| Tool | Version |
|---|---|
| gcc | 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1) |
| GNU Make | 4.3 |
| Python | 3.13.16 |
| NumPy | 2.5.3 |
| elan | 4.2.4 |
| Lean | 4.35.0 (commit eb6cafb) |
| Lake | 5.0.0-src+eb6cafb |
| Machine | 4 cores, 15 GB RAM, Linux x86_64 |

## What remains unfinished or is not machine-checked

1. **K=6 exact count** (`search/`): `./pangdp 6 …` reached 75 % after 2,802 s and the
   run ended without output (`scratchpad/dp6.err`, empty `dp6.out`);
   `results.json` records `words_le_6_letters: null`. Needs ≈ 1 h and 3.2 GB
   plus a sieve to 26⁶ on one core.
2. **Equation-pangram counts** (`search/`) are sampling estimates with standard
   errors, not exact counts; the 7-letter-word contribution (≈ 10⁷–10⁸) is
   itself an estimate.
3. **R(3,0) minimum** (`nicu-pangram/`): known to be 2 or 3; the exhaustive
   budget-2 search was stopped after 42 CPU-minutes. The witness searches for
   R(3,0) and R(0,3) were skipped on purpose (`--nowitness`).
4. **Not Lean-proved** (see `../checks/README.md` and `../wyrd/ROADMAP.md`):
   the complete list of 12 coupled-rule solutions, the 457,000 cutoff, and the
   non-existence of plain base-26 five-pair pangrams are computer searches
   with an informal soundness argument. Only "4296 is the smallest coupled
   sum" (plus parity, distinctness and the lower bound) is a theorem in
   `../wyrd/`.
5. **`../wyrd-mathlib/`** was not built in this session (it needs the ≈ 7 GB
   prebuilt Mathlib cache from `cache.mathlib.org`); only `../wyrd/` was built
   and audited, see above.
6. **`verify.js`, `verify2.js`, `roots.js`**: not present in either archive and
   not recoverable from this container.
