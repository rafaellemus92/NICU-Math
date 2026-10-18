# Independent cross-check and extensions

A second, independent treatment of the prime-pangram problem, written without
sight of the main study's code (Node and Python; sieve/trial-division and
Miller–Rabin primality; a memoised subset DP rather than Algorithm X or the
inclusion–exclusion engine).  Where the two studies ask the same question they
agree exactly; this directory also adds three things the main study does not
cover: natural-language number words, a smaller cluster list, and the two
scriptural alphabets with their native letter-numerals.

## 1. Cross-check on the main study's own lists (`crosscheck.js`)

`node crosscheck.js count` imports `../clusters.py` and applies the main
study's word rule exactly (onset ∈ ONSETS, nucleus = one vowel or an ordered
pair of distinct vowels, coda ∈ CODAS, letters distinct).

| quantity | main study | this implementation |
|---|---|---|
| pronounceable words | 289,404 | 289,404 |
| prime words | 16,243 | 16,243 (same length distribution 1/74/392/1,504/3,904/5,667/3,657/975/69) |
| every prime word ends in a letter coprime to 26 | yes | yes |
| perfect pangrams of prime words | 0 | 0 (exhaustive, 119,467 states, 0.5 s) |
| pronounceable pangrams with every word ending in a coprime letter | 0 | 0 (exhaustive, 4.5 s) |
| most consonants coverable by coprime-ending words | 17 | 17 (e.g. `ja ve zi qock brung dwylfths`, 23/26 letters) |
| N₀ = pronounceable pangrams ignoring primality | 353,750,976,000 | 353,750,976,000 (exact, 1,955,647 states, 339 s) |
| free CC·V·CC (one vowel), prime words | 34,587 | 34,587 (`verify.js`) |
| free CC·V·CC, perfect pangrams | 11,261,264,735,669 | 11,261,264,735,669 (exact, `verify.js`, 327 s) |
| N₀ free, closed form 20!·[x²⁰](1+x+x²)¹² | 2.9706 × 10²¹ | 2.971 × 10²¹ |

## 2. The same results on a smaller cluster list (`verify.js`, `verify2.js`)

`verify.js` carries its own, smaller English lists (70 onsets, ~75 codas, no
plural `-s` codas, no 4–5-letter codas) and an additional run rule (vowel runs
≤ 2, consonant runs ≤ 3).  Under those lists the dictionary is 4,644 prime
words and the conclusions are unchanged:

* no perfect pangram (exhaustive); N₀ = 20,596,550,400; refined first moment
  exactly 0, because 0 of the 32,112 coprime-ending words tile the alphabet
  (`verify2.js`);
* relaxation lattice: English onsets + any ≤ 2-consonant coda → solutions
  (`BAXQ DEVW FOJC LUMK ZYPS THRING`); any ≤ 2-consonant onset + English codas
  → solutions (`BHAK DXENG FVITS JPUQ MROC ZLYW`); either side alone suffices,
  in agreement with the main study's R(2,0) and R(0,2);
* free CC·V·CC: the same 34,587 words and the same count 11,261,264,735,669;
  refined first-moment estimate 1.716 × 10¹³ against the exact count (ratio
  0.66; the main study's exact weighted sum gives 1.108 × 10¹³, ratio 1.016 —
  the difference is this directory's cruder ln(value) ≈ (len − ½)·ln 26).

Seventh-vowel variants (W, or H, allowed as a nucleus under the small lists):
no perfect pangram either (5,217 and 5,318 prime words, exhaustive).

## 3. Natural languages (`primes.py`)

147 prime-number words from about 60 Latin-script languages (tagged for
romanisation, stripped diacritics, hyphenated compounds and constructed
languages), kept only when no letter repeats.  Exact cover finds no perfect
pangram at any level of permissiveness; the best disjoint covers are 21/26
(strict: `dwa peb cinq sju kolm trzy`, missing f g h v x) and 22/26 (with
romanisations and stripped diacritics: `panch bes du vijf kolm trzy`, missing
g q w x).  The reason is a counting bound: six vowel letters allow at most six
words, and no number word carries more than three consonants per vowel (four
in romanised Hindi *panch*), so at most 19 of the 20 consonants are reachable
even before letter collisions (knapsack over the list).

Real English words (Webster's 2nd, 234,450 entries → 2,366 prime-valued
isograms): no perfect pangram; best 22/26, `flaxy junk throw beg dimps`,
missing c q v z (`roots.js english`, needs a `words.txt` dump of the list).

## 4. Native letter-numerals: Koine Greek and Hebrew (`roots.js`)

Greek isopsephy (α=1 … ω=800) and Hebrew gematria (א=1 … ת=400) assign
numbers to letters natively, and a word's value is the *sum* of its letters.
Under a summation numeration the two positional congruences of the main study
are replaced by one parity rule: a prime word must have an odd value, hence an
odd number of odd-valued letters, and in both systems the only odd values are
the units 1, 3, 5, 7, 9 — five letters (α γ ε ζ θ; א ג ה ז ט).  So a prime
pangram has at most five words (plus the single even prime, β = ב = 2, which is
not a word), and the puzzle turns into packing the remaining letters into five
words.

* **Greek**, 24 letters (total 3999), Greek phonotactics (real onset clusters,
  diphthongs, and the rule that a word ends only in a vowel or ν ρ ς ξ ψ),
  words of ≤ 6 letters: 107,058 pronounceable prime words and **65,300 perfect
  pangrams (exact)**, every one with exactly five words, e.g.
  `βυζων (1259) · δμερ (149) · φθηψ (1217) · πτιγχο (1063) · σκλαξ (311)`.
  These are Greek-shaped nonsense, not attested Koine; a lexicon search is the
  natural next step.
* **Hebrew**, 22 letters (total 1495), words = roots of ≤ k letters, letters
  unordered within a root: k = 3 → **0**, k = 4 → **0**, k = 5 → 582,412,442.
  The bound is exact: five odd-letter roots of ≤ k letters hold at most
  5(k − 1) even letters (plus one for ב alone), and 17 even letters need k ≥ 5.
  Nothing shaped like a Hebrew root (2–4 letters) can do it.

## Running

```
node crosscheck.js count            # section 1 (≈ 6 min for the N0 count)
node --max-old-space-size=6144 verify.js ; node verify2.js    # section 2
python3 primes.py                   # section 3, natural languages
node roots.js greek 6 ; node roots.js hebrew 3 ; node roots.js hebrew 5   # section 4
# node roots.js english needs words.txt: one lower-case word per line (Webster's 2nd via the
# `english-words` PyPI package: get_english_words_set(['web2'], lower=True))
```
