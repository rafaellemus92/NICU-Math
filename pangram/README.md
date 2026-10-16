# Prime perfect pangrams: reproduction, relaxation, first moment, exact count

A *perfect pangram* here is a set of words that together use each of the 26
letters a–z exactly once.  Every word must be a prime number under the fixed
numeration and must be pronounceable.  Everything in this directory is
reproducible from the scripts; every number quoted below is printed by the
named script.

## Fixed definitions (not changed anywhere)

* **Numeration.** Bijective base 26, A=1 … Z=26: `AB = 1·26 + 2 = 28`
  (`core.value`).  Check values from the task statement:
  XWOZC = 11,382,491, TVYRQ = 9,543,577, KJUMS = 5,217,049, LFE = 8,273,
  BPI = 1,777, HDANG = 3,727,159 (asserted in `core.py`'s self test).
* **Vowels** a e i o u y (so y is never in a cluster); 20 consonants.
* **Vowel rule.** Every word contains at least one vowel; it is implied by
  the pronounceability rule below (the nucleus is non-empty).
* **Pronounceable** = onset + nucleus + coda, nucleus = one vowel or an
  ordered pair of two distinct vowels, onset ∈ ONSETS, coda ∈ CODAS (both
  lists contain the empty string).  Letters inside a word are distinct
  (forced by the pangram condition anyway).
* **Primality.** Deterministic Miller–Rabin with the 12 prime bases 2…37
  (`mr.c`, valid for all 64-bit n; the largest word value here is < 26¹⁰).
  No word is declared prime by fiat; `run_a_english.py` re-checks every
  dictionary entry with an independent pure-Python Miller–Rabin.

## The cluster lists (`clusters.py`)

The task statement left `[paste ONSETS]` / `[paste CODAS]` empty, so the lists
had to be fixed here.  They are orthographic English clusters, each with an
example word in `clusters.py`:

| list | size (incl. empty) | by length |
|---|---|---|
| ONSETS | 70 | 20 single letters (all consonants), 37 two-letter (bl br ch cl cr dr dw fl fr gh gl gn gr kn mn ph pl pn pr ps pt rh sc sh sk sl sm sn sp sq st sw th tr tw wh wr), 12 three-letter (chr phl phr sch scr shr sph spl spr str thr thw) |
| CODAS | 175 | 17 single letters (no final j, q, v), 65 two-letter, 72 three-letter, 18 four-letter, 2 five-letter (lfths, ngths) |

Two conventions matter for the results and are stated explicitly: `qu` is
onset `q` + vowel `u` (`squ` = onset `sq`), and no coda ends in `q`.  Because
the lists differ from the ones behind the "4,644 prime words" figure in the
task statement, the dictionary sizes below differ from 4,644; the *conclusions*
do not (see the structural argument, which is list-independent in spirit and
is re-checked against the lists by `structure.py`).

## Scripts

| script | what it does |
|---|---|
| `clusters.py` | the lists above |
| `core.py` | numeration, masks, primality (C helper `mr.c`), word generation for any regime, exact-cover search (Python, and the bitset C program `xcover.c`) |
| `engine.py` | exact counting of alphabet partitions into dictionary words: zeta transform over the 2²⁰ consonant subsets + inclusion–exclusion with a rank variable, modulo several 31-bit primes + CRT; the same code with float weights gives first-moment sums |
| `structure.py` | the packing bound that explains result (1) without any primality |
| `run_a_english.py` | task (a) |
| `run_b_lattice.py` | task (b), lattice of relaxations (mixed regimes R(o,c) and free regimes F(n,m)) |
| `reach.py`, `run_b_single.py` | task (b), the smallest *single* cluster whose addition creates a solution |
| `run_c_english.py` | task (c), English regime |
| `run_d_free_count.py`, `freedp.c` | task (d) and task (c) for the free regime; `freedp.c` is an independent second implementation of the count |

Reproduce everything (≈2 h on 4 cores, 8 GB RAM):

```
cd pangram
gcc -O2 -shared -fPIC -o libmr.so mr.c && gcc -O2 -o xcover xcover.c && gcc -O2 -o freedp freedp.c
python3 core.py && python3 engine.py            # self-tests (closed-form check of the engine)
python3 run_a_english.py
python3 structure.py
python3 run_d_free_count.py && ./freedp results/free_prime_masks.txt
python3 run_c_english.py
python3 run_b_lattice.py A ; python3 run_b_lattice.py B
for i in 0 1 2; do python3 reach.py $i; done ; python3 run_b_single.py 5
```
