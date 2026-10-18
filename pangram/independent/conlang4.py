"""Same dictionary as conlang3 (C0-2 V C0-2, prime), but a randomized rarest-letter-first
DFS with restarts — fast when solutions are plentiful."""
import itertools, time, random, sys
from conlang import ALPHA, VOW, value, is_prime
from primes import mask

CONS = [c for c in ALPHA if c not in VOW]
clusters = [""] + CONS + ["".join(p) for p in itertools.permutations(CONS, 2)]
t0 = time.time()
words = []
for on in clusters:
    for v in sorted(VOW):
        for co in clusters:
            w = on + v + co
            if len(set(w)) != len(w): continue
            if is_prime(value(w)): words.append(w)
items = [(w, mask(w)) for w in words]
FULL = (1 << 26) - 1
by_letter = {i: [it for it in items if it[1] >> i & 1] for i in range(26)}
order = sorted(range(26), key=lambda i: len(by_letter[i]))   # rarest letters first, fixed
print(f"{len(words):,} prime words; rarest letters: " + " ".join(f"{ALPHA[i]}:{len(by_letter[i])}" for i in order[:8]) + f"  (built in {time.time()-t0:.1f}s)")

def attempt(rnd, width=24, budget=20000):
    nodes = 0
    def rec(cov, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > budget: return None
        if cov == FULL: return list(chosen)
        for i in order:
            if not cov >> i & 1: break
        cands = [it for it in by_letter[i] if not it[1] & cov]
        if not cands: return None
        rnd.shuffle(cands)
        for w, m in cands[:width]:
            chosen.append(w); r = rec(cov | m, chosen); chosen.pop()
            if r: return r
        return None
    return rec(0, [])

rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
t0 = time.time(); found = []
for k in range(200):
    s = attempt(rnd)
    if s and s not in found:
        found.append(s)
        print(f"\n  {' '.join(w.upper() for w in s)}    (restart {k}, {time.time()-t0:.1f}s)")
        assert sorted(''.join(s)) == list(ALPHA)
        for w in s: print(f"     {w:6s} = {value(w):>10,}   prime: {is_prime(value(w))}")
    if len(found) >= 3 or time.time() - t0 > 240: break
print(f"\n{len(found)} solutions in {time.time()-t0:.1f}s over {k+1} restarts")
