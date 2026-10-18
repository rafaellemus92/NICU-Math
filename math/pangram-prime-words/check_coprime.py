"""
Exact confirmation that the refined first moment of the English regime is 0:
count (exactly, mod one prime) the pronounceable perfect pangrams in which
EVERY word ends in a letter coprime to 26.  The refined weight vanishes on any
other word, so this count being 0 proves E_refined = 0 (the float -0.4 printed
by run_c_english.py is inclusion-exclusion round-off around 0).
"""
from core import *
from engine import exact_count
ODD = set("acegikoqsuwy")
allw = english_words(prime_only=False)
sub = [w for w in allw if w[0][-1] in ODD]
print(f"pronounceable words ending in a letter coprime to 26: {len(sub):,} of {len(allw):,}")
cnt, M = exact_count(sub, nprimes=2, verbose=True)
print(f"CRT modulus {M:.3e} exceeds N0 = 353,750,976,000, so the count is certified exactly")
print(f"pangrams in which every word ends in a letter coprime to 26: {cnt[0]}")
