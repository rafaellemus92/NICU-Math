"""
Base-dependence experiment (not part of the fixed task): the English-cluster
regime (same ONSETS/CODAS, 1-2 vowels, A=1..Z=26 digits) read in another
numeration base b.  value(w) = sum d_i b^(k-i).  Because b^k = 0 (mod b), a
prime word must end in a letter whose digit is coprime to b, so the fraction
of admissible final letters is phi(b)/b - for a prime base there is no
constraint at all.  Reports dictionary size, exact number of perfect pangrams
(2 moduli, enough since the count is <= N0 = 353,750,976,000) and a witness.
usage: PANGRAM_BASE=29 python3 run_base_scan.py
"""
import json, math, os, time
from collections import Counter
from core import *
from engine import exact_count

b = BASE
t0 = time.time()
prime = english_words(prime_only=True)
coprime_finals = sorted(ch for ch in ALPHABET if math.gcd(ord(ch) - 96, b) == 1)
rec = {"base": b, "n_prime": len(prime), "admissible_final_letters": "".join(coprime_finals),
       "phi_over_b": f"{sum(1 for d in range(1, 27) if math.gcd(d, b) == 1)}/26 of the letter digits"}
print(f"base {b}: {len(prime):,} prime words; final letters coprime to {b}: {''.join(coprime_finals)} "
      f"({len(coprime_finals)} of 26); prime words by last letter: {dict(sorted(Counter(w[-1] for w,_,_ in prime).items()))}", flush=True)
sols, nodes = exact_cover_c(prime, max_solutions=1, tag=f"base{b}")
rec["witness"] = show(prime, sols[0]) if sols else None
print(f"  witness: {rec['witness']}  ({nodes:,} nodes)", flush=True)
cnt, M = exact_count(prime, nprimes=2, verbose=True)
rec["count"] = cnt[0]
print(f"  exact number of perfect pangrams of prime words, base {b}: {cnt[0]:,}  ({time.time()-t0:.0f}s)", flush=True)
os.makedirs("results/base_scan", exist_ok=True)
json.dump(rec, open(f"results/base_scan/base_{b}.json", "w"), indent=1)
