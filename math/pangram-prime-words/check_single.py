"""
Independent cross-check of the reach-table machinery (reach.py +
run_b_single.py): enumerate with the exact-cover program ALL perfect pangrams
whose dictionary is the English prime words plus the prime words with the
single added coda given on the command line (default 'jvq').  Only one word
can contain j, v and q, so every solution has exactly one foreign word, and
the total must equal the number reported by run_b_single.py for that cluster.
"""
import sys
from core import *
f = sys.argv[1] if len(sys.argv) > 1 else "jvq"
eng = english_words(prime_only=True)
extra = generate_words(ONSETS, nuclei(2), [f], prime_only=True)
words = eng + extra
sols, nodes = exact_cover_c(words, max_solutions=10 ** 9, tag="chk")
print(f"added coda '{f}': {len(extra)} prime words with it; perfect pangrams = {len(sols):,} ({nodes:,} nodes)")
for s in sols[:3]:
    print("  ", show(words, s))
