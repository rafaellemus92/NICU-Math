"""
Task (d): exact number of perfect pangrams under the free CC.V.CC rule
(onset = any 0-2 consonants, nucleus = exactly one vowel, coda = any 0-2
consonants, all words prime).  Also the first-moment numbers for (c).
"""
import json, math, time
from collections import Counter
from core import *
from engine import exact_count, weighted_sum, p_naive, p_refined

t0 = time.time()
allw = free_words(2, 2, 1, prime_only=False)
prime = free_words(2, 2, 1, prime_only=True)
print(f"free regime: pronounceable words {len(allw):,}, prime words {len(prime):,}")
print("  prime words by length:", dict(sorted(Counter(len(w) for w, _, _ in prime).items())))
print("  prime words by vowel:", dict(sorted(Counter([c for c in w if c in VOWELS][0] for w, _, _ in prime).items())))
# write per-vowel (consonant-mask, multiplicity) tables for the independent C check
with open("results/free_prime_masks.txt", "w") as f:
    for v in VOWELS:
        cnt = Counter(cmask(w) for w, _, _ in prime if v in w)
        f.write(f"{len(cnt)}\n")
        for m, c in sorted(cnt.items()):
            f.write(f"{m} {c}\n")

print("\nExact count via inclusion-exclusion engine (3 primes + CRT):")
cnt, M = exact_count(prime, nprimes=3, verbose=True)
print(f"  number of perfect pangrams (unordered sets of 6 words) = {cnt[0]:,}")
print(f"  as ordered sequences (x 6!) = {cnt[0]*720:,}")
print(f"  (CRT modulus {M:.3e} >> answer, and answer <= N0 = {math.factorial(20)*1221:,})")

print("\nFirst moment (task c, free regime):")
N0 = math.factorial(20) * 1221
E_naive = weighted_sum(allw, p_naive)[0]
E_ref = weighted_sum(allw, p_refined)[0]
print(f"  N0 (all pronounceable pangrams)      = {N0:.6e}")
print(f"  E_naive  = sum over pangrams prod 1/ln(n_i)                 = {E_naive:.6e}")
print(f"  E_refined = sum prod [last letter coprime to 26]*(13/6)/ln n = {E_ref:.6e}")
print(f"  observed exact count                                        = {cnt[0]:.6e}")
print(f"  ratios observed/E_naive = {cnt[0]/E_naive:.3f}, observed/E_refined = {cnt[0]/E_ref:.3f}")
json.dump({"n_pronounceable": len(allw), "n_prime": len(prime), "N0": N0, "count_unordered": cnt[0],
           "count_ordered": cnt[0]*720, "E_naive": E_naive, "E_refined": E_ref},
          open("results/d_free.json", "w"), indent=1)
print(f"done in {time.time()-t0:.0f}s")
