"""
Reachability / partial-cover tables for task (b).

For every vowel subset V' with |V'| in {4,5} (= the vowels NOT in a single
'foreign' word, which has 1-2 vowels) and every consonant subset C', compute

    R_{V'}[C'] = number of ways to partition V' u C' into ENGLISH prime words

exactly, modulo one prime (argv[1] selects which of engine.PRIMES).  Three
runs + CRT give the exact integer (the count is < 1e23 < product of moduli).

Method: in the zeta domain, H(S)(z) = sum over partitions pi of V' of
prod_B G_B(S)(z); then a Moebius transform over S for each z-degree, and the
diagonal R[C'] = [z^|C'|] H[C'] (the only tuples with union exactly C' and
total consonant count |C'| are the disjoint ones).
"""
import sys, time
import numpy as np
from core import *
from engine import build_G, _mul, zeta, PRIMES, popcount_table, NS, NC

pi = int(sys.argv[1])
p = PRIMES[pi]
t0 = time.time()
prime_words = english_words(prime_only=True)
G = build_G(prime_words, lambda w, v: 1, mod=p)
print(f"[{p}] G built for {len(prime_words):,} words in {time.time()-t0:.0f}s", flush=True)
pc = popcount_table()


def moebius(arr, mod):
    a = arr.reshape(-1, NS)
    for b in range(NC):
        v = a.reshape(a.shape[0], NS >> (b + 1), 2, 1 << b)
        v[:, :, 1, :] -= v[:, :, 0, :]
        v[:, :, 1, :] %= mod
    return arr


out = {}
for Vmask in range(64):
    vs = [i for i in range(6) if Vmask >> i & 1]
    if len(vs) not in (4, 5):
        continue
    acc = np.zeros((1, NC + 1, NS), dtype=np.int64)
    nm = [0]

    def rec(remaining, P):
        if not remaining:
            d = min(P.shape[1], NC + 1)
            acc[0, :d] += P[0, :d]
            acc[0, :d] %= p
            return
        v = remaining[0]
        for B in [1 << v] + [(1 << v) | (1 << w) for w in remaining[1:]]:
            if B not in G:
                continue
            rest = [u for u in remaining[1:] if not (B >> u & 1)]
            Q = G[B] if P is None else _mul(P, G[B], p, NC)
            nm[0] += 1
            rec(rest, Q)

    rec(vs, None)
    moebius(acc, p)
    R = acc[0][pc, np.arange(NS)]          # diagonal: z^|C| coefficient at C
    out[f"V{Vmask}"] = R.astype(np.int64)
    print(f"[{p}] V'={''.join(VOWELS[i] for i in vs)} products={nm[0]} nonzero={int((R!=0).sum()):,} "
          f"full={int(R[NS-1])} t={time.time()-t0:.0f}s", flush=True)

np.savez_compressed(f"results/reach_mod{pi}.npz", **out)
print(f"[{p}] saved results/reach_mod{pi}.npz in {time.time()-t0:.0f}s")
