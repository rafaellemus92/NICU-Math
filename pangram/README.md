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
python3 run_b_lattice.py B                         # free family, n+m <= 5
python3 run_b_lattice.py "R(0,0)" "R(1,0)" "R(0,1)" "R(1,1)" "R(2,0)" "R(0,2)" "R(2,1)" "R(1,2)" "R(2,2)"
python3 run_b_lattice.py "R(3,0)" "R(0,3)" --nowitness   # witness search skipped (see notes)
for i in 0 1 2; do python3 reach.py $i; done ; python3 run_b_single.py 5
python3 check_single.py jvq ; python3 check_onset3.py 3 ; python3 check_onset3.py 4 ; python3 check_coprime.py
python3 summarize.py                                # regenerates the lattice tables from results/b_lattice/*.json
```

(The R regimes with o, c ≤ 2 use `--minbudget` = the b.1 result that no
single ≤ 2-consonant cluster works, so their witness search starts at the
packing lower bound; total wall time for everything is about 3 hours on
4 cores.)

## (a) Reproduction of result (1): no solution under the English lists

`python3 run_a_english.py` (about 10 s):

| quantity | value |
|---|---|
| pronounceable words (onset+nucleus+coda, distinct letters) | 289,404 |
| of which prime (the dictionary) | **16,243** |
| prime words by length 1/2/3/4/5/6/7/8/9 | 1 / 74 / 392 / 1,504 / 3,904 / 5,667 / 3,657 / 975 / 69 |
| prime words with 1 / 2 vowels | 3,142 / 13,101 |
| exact-cover search nodes (bitset Algorithm X, `xcover.c`) | 1,633,290 (2,805,970 without the consonant-capacity prune added later to `xcover.c`) |
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
word that ends in a letter not coprime to 26, and **no pronounceable pangram
at all has every word ending in a letter coprime to 26**: every vowel index
is coprime to 26, so such a pangram would be exactly a cover of the 20
consonants by ≤ 6 English onsets and ≤ 6 odd codas, which the packing DP of
`structure.py` rules out (at most 17 consonants).  `check_coprime.py` is a
consistency check of the same statement with the counting engine: the number
of such pangrams (137,556 of the 289,404 pronounceable words end in a coprime
letter) is 0 modulo two 31-bit primes whose product 4.6 × 10¹⁸ exceeds N₀,
so the engine count is certified to be exactly 0.  (`run_c_english.py`
prints E_refined = -0.41: that is float64 round-off of an alternating
inclusion–exclusion sum whose individual terms are ~10¹⁵; the exact value is
0.)  Average prime probability per pangram in the two regimes:
E_naive/N₀ = 2.0 × 10⁻⁷ (English) and 2.1 × 10⁻⁷ (free), so the regimes
differ not in how likely a random pronounceable pangram is to be all-prime,
but in whether the residue structure allows any at all: English N₀ is 10¹⁰
times smaller than the free N₀ *and* every one of its pangrams is killed by
the mod-26 constraint.

## (b) Minimal relaxation

### b.1 Add a single cluster to the English lists

`reach.py` + `run_b_single.py`.  A solution with exactly one non-English
cluster is one word `f+nucleus+e` or `e+nucleus+f` (e an English cluster or
empty, f a string of k distinct consonants) plus a partition of the other
letters into English prime words.  `reach.py` computes, for each of the 21
vowel subsets of size 4–5 and each consonant subset, the exact number of
English-prime-word partitions (three moduli + CRT); `run_b_single.py` then
tries every (nucleus, e, k-subset) whose complement is coverable and every
ordering of the k consonants (`run_b_single.py 4` takes about a minute and
writes `results/b_single_cluster.json`; k = 5 takes 35 minutes, and its
summary line is kept in `results/b_single_k5.txt`).

| k = length of the added cluster | (nucleus, e, consonant-set) with coverable complement | prime foreign words | distinct added clusters that work | solutions with exactly one foreign cluster |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 2,011 | 0 | 0 | 0 |
| 3 | 80,801 | 1,599 | **100** | **946,514** |
| 4 | 1,041,654 | 213,826 | 15,022 | 92,916,257 |
| 5 | 6,489,500 | 9,556,451 | 558,205 | 4,128,113,285 |

So **the smallest single addition is a 3-consonant coda ending in `q`**, and
no 1- or 2-consonant cluster (onset or coda) suffices.  Both short cases
fail structurally, not by a primality coincidence: with k = 1 there is not
even a letter packing (0 coverable complements, as the capacity bound
predicts); with k = 2 the reach tables list 2,011 coverable configurations,
but every one of them puts the foreign cluster in the *onset* with an English
coda ending in h, z, t, b or p (921 / 378 / 376 / 168 / 168 configurations),
all even letters, so every candidate word is even; no coverable configuration
with a foreign 2-coda exists at all.  Among the 100 working 3-codas, 68 contain one of
`j v x z` and 32 do not (e.g. `dfq` 8,006 solutions, `bmq` 6,058, `bfq`
5,986): what matters is that `q`, which is coprime to 26, can *end* a word,
so `q` leaves the onset slot it is forced into by the English lists.  At
k = 4 the 15,022 working clusters split into 7,294 codas (ending in
c, g, k, q or w; 69,161,901 solutions) and 7,728 onsets (23,754,356
solutions).  All 100 working 3-clusters are
codas ending in `q` (`check_onset3.py 3`: no 3-consonant *onset* works at all, 0 prime
foreign words among 60,649 coverable configurations; the smallest single added
*onset* that works has 4 consonants, e.g. `qvjx`, 7,728 such onsets, 23,754,356
solutions, `check_onset3.py 4`): `q` is coprime to 26, so a coda ending
in `q` is allowed arithmetically, and it lets two of the "onset-only" letters
`j v x z` ride inside a coda, which is exactly what the packing bound said
was missing.  The most productive additions are `jvq` (38,093 solutions),
`vzq` (37,750), `vjq` (34,951), `jxq` (29,656), `zxq` (28,703).  Witnesses
(each line is a complete perfect pangram of prime words; the word ending in
`q` carries the foreign coda, every other cluster is English):

* ZA XEG DYJVQ FLOK BRIMPTS WHUNC — values 677 / 16,361 / 2,274,653 / 113,969 / 836,048,947 / 10,665,619
* ZA XEG DYJVQ FONC BLIMPHS TRUWK — values 677 / 16,361 / 2,274,653 / 115,963 / 764,760,379 / 9,470,693
* ZA XEG DYJVQ FLINC BUWK THROMPS — values 677 / 16,361 / 2,274,653 / 2,959,219 / 49,957 / 6,281,864,959

* BAXDQ VE ZYC JONG FLUMPTS RHIWK — values 947,873 / 577 / 18,229 / 186,271 / 2,005,907,507 / 8,372,869 (foreign coda `xdq`)
* BAVFQ ZO JUC MYXTHS DWENK PLIRG — values 946,573 / 691 / 7,309 / 166,317,859 / 2,235,907 / 7,529,087 (foreign coda `vfq`)

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

| regime | prime words | packing feasible | min non-English clusters | exact number of solutions | witness |
|---|---|---|---|---|---|
| R(0,0) | 16,243 | no (⇒ 0) | — | 0 | — |
| R(1,0) | 16,243 | no (⇒ 0) | — | 0 | — |
| R(0,1) | 16,641 | no (⇒ 0) | — | 0 | — |
| R(1,1) | 16,641 | no (⇒ 0) | — | 0 | — |
| R(2,0) | 108,593 | yes | 3 | 8,627,591,390 ≈ 8.63 × 10^09 | VE QA BZYC XJIWK DPURG MNOLFTHS |
| R(0,2) | 40,546 | yes | 2 | 475,567,462 ≈ 4.76 × 10^08 | VE ZA JOBG DWYXQ FLUMPTS CHRINK |
| R(2,1) | 110,624 | yes | 3 | 27,117,653,723 ≈ 2.71 × 10^10 | VE ZA BJUC XMONG DQYLFTHS PRIWK |
| R(1,2) | 40,546 | yes | 2 | 475,567,462 ≈ 4.76 × 10^08 | VE ZA JOBG DWYXQ FLUMPTS CHRINK |
| R(2,2) | 241,381 | yes | 2 | 20,886,836,221,201 ≈ 2.09 × 10^13 | ZA VE BJYG FLOXQ DWUMPTS CHRINK |
| R(3,0) | 1,418,985 | yes | 2 or 3 (see note) | 949,086,562,609,181 ≈ 9.49 × 10^14 | VE QA BZYC XJIWK DPURG MNOLFTHS (the R(2,0) witness) |
| R(0,3) | 435,022 | yes | 1 (b.1) | 19,884,222,065,476 ≈ 1.99 × 10^13 | ZA XEG DYJVQ FLOK BRIMPTS WHUNC (from b.1) |

Notes on the R table.  "min non-English clusters" is exact where a number is
given: the cost-aware packing DP (`structure.packing_min_foreign`) gives a
lower bound and the exact-cover search found a witness attaining it.  R(1,0)
adds nothing (every single consonant is already an English onset) and R(0,1)
only adds the single codas j, q, v; both stay packing-infeasible.  R(1,2) is
the same dictionary as R(0,2).  For R(0,3) the minimum is 1 by section b.1
(a single 3-coda ending in q suffices, 0 is the English case).  For R(3,0)
the minimum is 2 or 3: it is not 1 (no single 3-consonant onset works,
`check_onset3.py 3`), the R(2,0) witness with three 2-letter foreign onsets
is also an R(3,0) solution, and the exhaustive budget-2 search (two foreign
onsets of ≤ 3 letters) was stopped after 42 CPU-minutes without finishing,
so that case is left open.

| regime (free family, one vowel per word) | prime words | exact number of solutions | witness |
|---|---|---|---|
| F(1,1) | 228 | 0 | — |
| F(0,3) | 2,414 | 0 | — |
| F(1,2) | 2,614 | 0 | — |
| F(2,1) | 2,966 | 0 | — |
| F(3,0) | 7,816 | 0 | — |
| F(0,4) | 32,121 | 252,992,298,224 ≈ 2.53 × 10^11 | ERC APK YBDZG IFHLQ OJMVW UXTNS |
| F(1,3) | 34,231 | 2,787,766,399,849 ≈ 2.79 × 10^12 | XAC ZEG RYBDS TUFHK LOJMQ PINVW |
| F(2,2) | 34,587 | 11,261,264,735,669 ≈ 1.13 × 10^13 | ZA BROC JMYDG HXIFK PTULQ SVENW |
| F(3,1) | 39,362 | 206,104,093,487,571 ≈ 2.06 × 10^14 | NI BDVU FHXEC JKMOG LPTAQ WRZYS |
| F(4,0) | 105,501 | 6,632,950,416,638,335 ≈ 6.63 × 10^15 | BO CDWI FGHTE JKLMU NPQZA RSVXY |
| F(0,5) | 425,147 | 11,913,392,779,963 ≈ 1.19 × 10^13 | YC UK EBTG ODFHLS AJMPVQ INZRXW |
| F(1,4) | 450,883 | 603,962,334,877,113 ≈ 6.04 × 10^14 | BU CY TIDS ZAFGPK VEHJLQ NOMXRW |
| F(2,3) | 453,441 | 3,421,738,179,441,134 ≈ 3.42 × 10^15 | E BO FXICG MRYDHK NWAJLQ TVUPZS |
| F(3,2) | 458,401 | 16,417,633,268,700,800 ≈ 1.64 × 10^16 | BI CY DGTA HLNOFK MZPUJQ XVWERS |
| F(4,1) | 523,930 | 76,380,875,883,311,234 ≈ 7.64 × 10^16 | E BU CDFZY HJLMIG NPQTOK VXRWAS |
| F(5,0) | 1,396,507 | 128,575,945,396,019,880 ≈ 1.29 × 10^17 | BO CY DFMA GHJLTI KNPVSE QRXZWU |

**Reading the lattice.**

* *Codas are the bottleneck, onsets are cheap.*  Relaxing only the codas to
  arbitrary 2-consonant strings (R(0,2)) already gives 4.8 × 10⁸ solutions,
  needing 2 foreign codas (one of them ending in q); relaxing only the onsets
  to 2 consonants (R(2,0)) gives 8.6 × 10⁹ but needs three foreign onsets.
  Neither R(1,1) nor the 1-letter relaxations help at all (packing bound).
  The minimal elements of the R lattice with solutions are therefore R(2,0)
  and R(0,2); counted in *added clusters*, the single 3-coda of b.1 (one
  cluster, R(0,3) with budget 1) is the minimal relaxation.
* *Why.*  Every word must end in a vowel or in c, g, k, q, s, w, while j, q,
  v, x, z never appear in English odd codas; so under the English lists
  j, q, v, z (and x) are pinned to five separate onset slots and the
  remaining 15 consonants do not fit in the odd codas (max 17 consonants in
  total, `structure.py`).  Any relaxation that frees one of those pins
  (a coda ending in q, or an onset `bz`/`xj`) buys the missing capacity.
* *Free family (the task's regime (2) is F(2,2)).*  Nothing with n + m ≤ 3
  works (6 words × 3 consonants = 18 < 20).  All five regimes with
  n + m = 4 have solutions, so F(2,2) is one of five minimal free regimes.
  The counts are wildly asymmetric: F(4,0) (onsets only, every word ends in
  its vowel, which is always coprime to 26) has 6.6 × 10¹⁵ solutions, F(0,4)
  only 2.5 × 10¹¹, because a non-empty coda must end in one of just six
  letters.  Counts grow monotonically along the lattice, as they must
  (F(2,2) ⊂ F(3,2) ⊂ … ), which is a consistency check on the engine.
* *The task's regime (2).*  R(2,2) (English lists plus all ≤ 2-consonant
  clusters, 1–2 vowels) has 2.09 × 10¹³ solutions and needs 2 foreign
  clusters; F(2,2) (exactly one vowel, no English clusters of length 3+)
  has 1.13 × 10¹³, the number asked for in task (d).
