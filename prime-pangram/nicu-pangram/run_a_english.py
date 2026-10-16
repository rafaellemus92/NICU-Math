"""
Task (a): reproduce result (1) -- no perfect pangram of prime words under the
English onset/coda clusters in clusters.py.

Prints the dictionary size and runs an exhaustive exact-cover search.
"""
import json, time
from collections import Counter
from core import *

t0 = time.time()
allw = english_words(prime_only=False)
prime = english_words(prime_only=True)
print(f"pronounceable words (onset+nucleus+coda, distinct letters): {len(allw):,}")
print(f"prime words: {len(prime):,}")
print(f"  by length: {dict(sorted(Counter(len(w) for w,_,_ in prime).items()))}")
print(f"  by number of vowels: {dict(sorted(Counter(sum(ch in VOWELS for ch in w) for w,_,_ in prime).items()))}")
last = Counter(w[-1] for w, _, _ in prime)
print(f"  last letters of prime words: {dict(sorted(last.items()))}")
print(f"  letters that occur in at least one prime word: {''.join(sorted(set(''.join(w for w,_,_ in prime))))}")
# sanity: every prime word has a vowel and distinct letters
assert all(any(ch in VOWELS for ch in w) and len(set(w)) == len(w) for w, _, _ in prime)
assert all(is_prime_py(v) and v == value(w) for w, v, _ in prime)

print("\nExhaustive exact-cover search (bitset Algorithm X, xcover.c) over the prime dictionary ...")
sols, nodes = exact_cover_c(prime, max_solutions=10 ** 9, tag="a")
print(f"  search nodes: {nodes:,}   perfect pangrams found: {len(sols)}")
for s in sols[:20]:
    print("  ", show(prime, s))

# Structural facts used in the README
odd = set("acegikoqsuwy")   # letters coprime to 26
print("\nStructural checks:")
print("  every prime word ends in a letter coprime to 26:",
      all(w[-1] in odd for w, _, _ in prime))
for L in "jqvxz":
    in_onset = sum(1 for w, _, _ in prime if L in w and w.index(L) < [i for i, ch in enumerate(w) if ch in VOWELS][0])
    in_coda = sum(1 for w, _, _ in prime if L in w and w.index(L) > [i for i, ch in enumerate(w) if ch in VOWELS][-1])
    print(f"  '{L}': in onset of {in_onset} prime words, in coda of {in_coda} prime words")

json.dump({"n_pronounceable": len(allw), "n_prime": len(prime), "solutions": len(sols), "nodes": nodes},
          open("results/a_english.json", "w"), indent=1)
with open("results/english_prime_words.txt", "w") as f:
    for w, v, _ in sorted(prime):
        f.write(f"{w} {v}\n")
print(f"\ndone in {time.time()-t0:.1f}s; prime dictionary written to results/english_prime_words.txt")
