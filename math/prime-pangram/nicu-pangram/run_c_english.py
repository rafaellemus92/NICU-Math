"""
Task (c), English regime: exact N0 (number of pronounceable perfect pangrams,
primality ignored) and the first-moment estimates
    E_naive   = sum over pangrams of prod_i 1/ln(n_i)
    E_refined = sum over pangrams of prod_i [last letter coprime to 26] (13/6)/ln(n_i)
Also re-derives the exact number of all-prime pangrams (0) with the counting
engine as a second, independent confirmation of task (a).
"""
import json, math, time
from collections import Counter
from core import *
from engine import exact_count, weighted_sum, p_naive, p_refined

t0 = time.time()
allw = english_words(prime_only=False)
prime = english_words(prime_only=True)
print(f"English regime: pronounceable words {len(allw):,}, prime words {len(prime):,}")
print("  words by number of consonants:", dict(sorted(Counter(len(w)-sum(c in VOWELS for c in w) for w,_,_ in allw).items())))

print("\nExact N0 (4 primes + CRT):")
cnt, M = exact_count(allw, nprimes=4, verbose=True)
N0 = cnt[0]
print(f"  N0 = {N0:,}  ({N0:.4e}); CRT modulus {M:.2e}")

print("\nExact count of all-prime pangrams via the engine (should be 0, as in task a):")
pc, _ = exact_count(prime, nprimes=2, verbose=True)
print(f"  prime pangrams = {pc[0]}")

print("\nFirst moment:")
E_naive = weighted_sum(allw, p_naive)[0]
E_ref = weighted_sum(allw, p_refined)[0]
print(f"  E_naive   = {E_naive:.6e}")
print(f"  E_refined = {E_ref:.6e}")
print(f"  observed  = {pc[0]}")
json.dump({"n_pronounceable": len(allw), "n_prime": len(prime), "N0": N0, "prime_pangrams": pc[0],
           "E_naive": E_naive, "E_refined": E_ref}, open("results/c_english.json", "w"), indent=1)
print(f"done in {time.time()-t0:.0f}s")
