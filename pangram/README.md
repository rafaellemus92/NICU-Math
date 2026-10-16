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

## (a) Reproduction of result (1): no solution under the English lists

`python3 run_a_english.py` (13 s):

| quantity | value |
|---|---|
| pronounceable words (onset+nucleus+coda, distinct letters) | 289,404 |
| of which prime (the dictionary) | **16,243** |
| prime words by length 1/2/3/4/5/6/7/8/9 | 1 / 74 / 392 / 1,504 / 3,904 / 5,667 / 3,657 / 975 / 69 |
| prime words with 1 / 2 vowels | 3,142 / 13,101 |
| exact-cover search nodes (bitset Algorithm X, `xcover.c`) | 2,805,970 |
| perfect pangrams of prime words | **0** |

The dictionary is 16,243 words rather than 4,644 because my lists are
larger (every plural `-s` coda such as `lks`, `mpts`, `ngths` is included, and
both orders of a two-vowel nucleus are allowed).  The search is exhaustive;
`run_c_english.py` recomputes the same count (0) with the completely different
inclusion–exclusion engine as a cross-check.

**Why it is impossible, independently of which numbers are prime**
(`structure.py`).  Since 26^k ≡ 0 (mod 26), the value of a word is congruent
to its last letter mod 26, so a prime word of two or more letters ends in a
letter coprime to 26: `a c e g i k o q s u w y`.  Hence every non-empty coda of
a prime word ends in `c g k q s w` ("odd coda"); only 90 of the 174 non-empty
English codas qualify, and none of them contains `j q v z` (only `xts`/`xths`
contain `x`).  A perfect pangram has at most 6 words (one or two vowels each),
so the 20 consonants must be exactly covered by ≤ 6 letter-disjoint English
onsets plus ≤ 6 letter-disjoint odd codas.  A subset DP over the 2²⁰
consonant subsets shows that the most such a configuration can hold is
**17 consonants** (`structure.py`), three short of 20.  So result (1) is a
packing obstruction: the letters `j q v z` can only be onsets, each word has
one onset, and the odd codas are too short to absorb the rest.  Every prime
word in the dictionary indeed ends in a letter coprime to 26, and `j q v z`
occur only in onsets (printed by `run_a_english.py`).

## (d) Exact count under the free CC·V·CC rule

Regime (2) of the task: onset = any 0–2 distinct consonants, nucleus = one
vowel, coda = any 0–2 distinct consonants.  `python3 run_d_free_count.py` (42 s):

| quantity | value |
|---|---|
| pronounceable words | 786,846 |
| prime words | **34,587** (by length 1/2/3/4/5: 1 / 67 / 883 / 4,401 / 29,235) |
| perfect pangrams, unordered sets of 6 words | **11,261,264,735,669** ≈ 1.126 × 10¹³ |
| as ordered sequences (× 6!) | 8,108,110,609,681,680 |

The count is exact: the engine evaluates the disjoint-union product of the six
per-vowel word tables at the full consonant set by inclusion–exclusion with a
rank variable, modulo three 31-bit primes, and recombines by CRT (the answer
is far below the 9.9 × 10²⁷ CRT modulus).  Two independent confirmations:

* `freedp.c` (a plain stage-by-stage DP over 2²⁰ consonant subsets, 64-bit
  integers, no inclusion–exclusion) prints the same `11261264735669`;
* with primality switched off the engine returns exactly the closed form
  N₀ = 20!·[x²⁰](1+x+x²)¹² = 20!·1221 = 2,970,573,351,983,677,440,000
  (`python3 engine.py`).

Every solution has exactly six words (each word has exactly one vowel) and
every word ends in a letter coprime to 26; the task's example
XWOZC TVYRQ KJUMS LFE BPI HDANG is one of the 1.1 × 10¹³.

## (c) First-moment estimates

For a set of pangrams P (primality ignored) the first moment is
E = Σ_{p∈P} Π_{w∈p} P(w prime).  Two densities are used:

* naive: P(n prime) = 1/ln n;
* refined: the value is ≡ last letter (mod 26), so P = 0 unless the last
  letter is coprime to 26, and then P = (26/φ(26))/ln n = (13/6)/ln n.

Both sums are computed exactly over all pangrams by the same engine with
float weights (`engine.weighted_sum`; the 0/1-weight version reproduces the
integer counts, and the all-ones version reproduces N₀ to 3 × 10⁻⁸).

| regime | N₀ (pronounceable pangrams) | E_naive | E_refined | observed |
|---|---|---|---|---|
| English clusters (1–2 vowels) | 353,750,976,000 ≈ 3.54 × 10¹¹ | 7.06 × 10⁴ | **0 (exact)** | 0 |
| free CC·V·CC (1 vowel) | 2.9706 × 10²¹ | 6.193 × 10¹⁴ | 1.108 × 10¹³ | 1.126 × 10¹³ |

The refined first moment predicts the free-regime count to within 1.6 %
(observed / E_refined = 1.016); the naive one is 55× too high because it
ignores that half of all words are even and 1/13 are divisible by 13.
For the English regime the naive first moment, N₀ × (average of Π 1/ln nᵢ)
= 7.1 × 10⁴, would predict tens of thousands of solutions, so the observed 0
is *not* a fluctuation of a fair model: the model is wrong.  The refined
first moment is exactly 0, because the refined density vanishes on every
word that ends in a letter not coprime to 26, and `check_coprime.py` proves
(exact count, 0 mod a 31-bit prime, 137,556 of the 289,404 pronounceable
words end in a coprime letter) that **no pronounceable pangram at all has
every word ending in a letter coprime to 26** - the packing obstruction of
`structure.py` again.  (`run_c_english.py` prints E_refined = -0.41: that is
float64 round-off of an alternating inclusion–exclusion sum whose individual
terms are ~10¹⁵; the exact value is 0.)  Average prime probability per
pangram in the two regimes: E_naive/N₀ = 2.0 × 10⁻⁷ (English) and
2.1 × 10⁻⁷ (free), so the regimes differ not in how likely a random
pronounceable pangram is to be all-prime, but in whether the residue
structure allows any at all: English N₀ is 10¹⁰ times smaller than the free
N₀ *and* every one of its pangrams is killed by the mod-26 constraint.

## (b) Minimal relaxation

### b.1 Add a single cluster to the English lists

`reach.py` + `run_b_single.py`.  A solution with exactly one non-English
cluster is one word `f+nucleus+e` or `e+nucleus+f` (e an English cluster or
empty, f a string of k distinct consonants) plus a partition of the other
letters into English prime words.  `reach.py` computes, for each of the 21
vowel subsets of size 4–5 and each consonant subset, the exact number of
English-prime-word partitions (three moduli + CRT); `run_b_single.py` then
tries every (nucleus, e, k-subset) whose complement is coverable and every
ordering of the k consonants.

| k = length of the added cluster | (nucleus, e, consonant-set) with coverable complement | prime foreign words | distinct added clusters that work | solutions with exactly one foreign cluster |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 2,011 | 0 | 0 | 0 |
| 3 | 80,801 | 1,599 | **100** | **946,514** |
| 4 | 1,041,654 | 213,826 | 15,022 | 92,916,257 |
| 5 | <<K5>> | | | |

So **the smallest single addition is a 3-consonant coda**, and no 1- or
2-consonant cluster (onset or coda) suffices.  All 100 working 3-clusters are
codas ending in `q` <<K3_ONSET_NOTE>>: `q` is coprime to 26, so a coda ending
in `q` is allowed arithmetically, and it lets two of the "onset-only" letters
`j v x z` ride inside a coda, which is exactly what the packing bound said
was missing.  The most productive additions are `jvq` (38,093 solutions),
`vzq` (37,750), `vjq` (34,951), `jxq` (29,656), `zxq` (28,703).  Witnesses
(each line is a complete perfect pangram of prime words; the first word
carries the foreign coda):

* ZA XEG DYJVQ FLOK BRIMPTS WHUNC — values 677 / 16,361 / 2,274,653 / 113,969 / 836,048,947 / 10,665,619
* ZA XEG DYJVQ FONC BLIMPHS TRUWK — values 677 / 16,361 / 2,274,653 / 115,963 / 764,760,379 / 9,470,693
* ZA XEG DYJVQ FLINC BUWK THROMPS — values 677 / 16,361 / 2,274,653 / 2,959,219 / 49,957 / 6,281,864,959

(Checked by `check_single.py jvq`, which enumerates by exact cover *all*
38,093 perfect pangrams whose only non-English cluster is the coda `jvq` -
the same number the reach tables give for that cluster, an independent
confirmation of the table machinery.)

### b.2 Lattice of regimes

`run_b_lattice.py`.  R(o,c) = English lists plus *all* consonant strings of
length ≤ o as onsets and ≤ c as codas (nucleus 1–2 vowels); F(n,m) = the
free family of the task (onset ≤ n, one vowel, coda ≤ m).  "min foreign" is
the smallest number of non-English clusters any solution uses (exact-cover
search with a cost budget).  "packing" is the structural bound of
`structure.py` applied to the regime's lists (False ⇒ provably 0).

| regime | prime words | packing | min foreign clusters | exact number of solutions |
|---|---|---|---|---|
<<LATTICE_A>>

| regime (free family) | prime words | packing | exact number of solutions |
|---|---|---|---|
<<LATTICE_B>>

<<LATTICE_COMMENT>>
