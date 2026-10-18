"""Constructive version: build the dictionary of pronounceable prime words
(onset + nucleus + coda, distinct letters, value prime in bijective base-26),
then exact-cover the alphabet with them."""
import itertools, sys, time
from conlang import ALPHA, VOW, ONSETS, CODAS, value, is_prime, pronounceable
from primes import solve, mask

CONS = [c for c in ALPHA if c not in VOW]
vowels = sorted(VOW)
nuclei = vowels + ["".join(p) for p in itertools.permutations(vowels, 2)]

t0 = time.time()
words = set()
for on in ONSETS:
    for nu in nuclei:
        for co in CODAS:
            w = on + nu + co
            if len(set(w)) != len(w): continue
            if not is_prime(value(w)): continue
            if not pronounceable(w): continue
            words.add(w)
words = sorted(words, key=lambda w: (-len(w), w))
print(f"{len(words):,} pronounceable prime words (built in {time.time()-t0:.1f}s); longest: {' '.join(words[:6])}")
by_len = {}
for w in words: by_len[len(w)] = by_len.get(len(w), 0) + 1
print("by length:", dict(sorted(by_len.items())))

t0 = time.time()
sols, _ = solve(words)
print(f"exact cover: {len(sols)} solution found in {time.time()-t0:.1f}s")
for s in sols[:3]:
    print("\n  " + " ".join(w.upper() for w in s))
    assert sorted("".join(s)) == list(ALPHA)
    for w in s:
        print(f"     {w:8s} = {value(w):>14,}   prime: {is_prime(value(w))}   pronounceable: {pronounceable(w)}")

# how many distinct solutions exist? count up to a limit by continuing the search
def count_solutions(words, limit=2000):
    items = [(w, mask(w)) for w in words]
    FULL = (1 << 26) - 1
    by_letter = {i: [it for it in items if it[1] >> i & 1] for i in range(26)}
    n = 0
    def rec(cov):
        nonlocal n
        if n >= limit: return
        if cov == FULL: n += 1; return
        best = None
        for i in range(26):
            if cov >> i & 1: continue
            c = [it for it in by_letter[i] if not it[1] & cov]
            if best is None or len(c) < len(best): best = c
            if not c: return
        for w, m in best: rec(cov | m)
    rec(0)
    return n
t0 = time.time()
print(f"\ndistinct solutions (search capped at 2000): {count_solutions(words)} in {time.time()-t0:.1f}s")
