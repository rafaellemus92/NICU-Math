"""Does any single added ONSET of length k (default 3) yield a solution?
Same method as run_b_single.py, restricted to foreign onsets."""
import itertools, sys
import numpy as np
from core import *
from engine import crt, PRIMES, NS
k = int(sys.argv[1]) if len(sys.argv) > 1 else 3
tabs = [np.load(f"results/reach_mod{i}.npz") for i in range(3)]
VB = {v: 1 << i for i, v in enumerate(VOWELS)}
FULLC = NS - 1
subs = np.array([sum(1 << i for i in c) for c in itertools.combinations(range(20), k)], dtype=np.int64)
reachable = prime_words = 0
clusters = {}
for nu in nuclei(2):
    Vp = 63 ^ sum(VB[v] for v in nu)
    rs = [t[f"V{Vp}"] for t in tabs]
    reach = (rs[0] != 0) | (rs[1] != 0) | (rs[2] != 0)
    for e in CODAS:
        if set(e) & set(nu):
            continue
        em = cmask(e)
        ok = subs[(subs & em) == 0]
        comp = FULLC ^ em ^ ok
        good = ok[reach[comp]]
        reachable += len(good)
        for Kf in good:
            letters = [CONS_LIST[i] for i in range(20) if Kf >> i & 1]
            C = FULLC ^ em ^ int(Kf)
            for perm in itertools.permutations(letters):
                f = "".join(perm)
                if f in ONSETS:
                    continue
                w = f + nu + e
                if is_prime_py(value(w)):
                    prime_words += 1
                    R = crt([int(r[C]) for r in rs], PRIMES[:3])[0]
                    clusters[f] = clusters.get(f, 0) + R
print(f"foreign ONSETS of length {k}: reachable (nucleus,coda,set) = {reachable:,}; prime foreign words = {prime_words:,}; "
      f"onsets giving solutions = {len(clusters)}; total solutions = {sum(clusters.values()):,}")
print(sorted(clusters.items(), key=lambda kv: -kv[1])[:10])
