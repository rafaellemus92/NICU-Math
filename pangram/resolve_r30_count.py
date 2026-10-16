"""Step 2: exact number of R(3,0) solutions by number of non-English onsets (0, 1, 2)."""
import sys, time, json
from core import *
from engine import exact_count, PRIMES, crt
nprimes = int(sys.argv[1]) if len(sys.argv) > 1 else 2
t0 = time.time()
onsets = sorted(set(ONSETS) | set(free_clusters(3)), key=lambda s: (len(s), s))
words = generate_words(onsets, nuclei(2), CODAS, prime_only=True, with_tags=True)
eo = set(ONSETS)
tagged = [(w, v, m, 0 if o in eo else 1) for (w, v, m, o, c) in words]
print(f"R(3,0): {len(tagged):,} prime words, {sum(1 for t in tagged if t[3])} with a non-English onset ({time.time()-t0:.0f}s)", flush=True)
res = []
known = {}
try:
    known = {int(k): v for k, v in json.load(open("results/r30_residues.json")).items()}
except Exception:
    pass
for i in range(nprimes):
    if PRIMES[i] in known:          # residue already computed by an earlier run
        res.append([0, 0, known[PRIMES[i]]])
        print(f"  mod {PRIMES[i]}: reusing recorded residues {res[-1]}", flush=True)
        continue
    cnt, M = exact_count(tagged, max_cost=2, nprimes=i + 1, verbose=True, word_cost_max=1) if False else (None, None)
    # run one prime at a time so partial results are visible
    from engine import build_G, count_partitions
    p = PRIMES[i]
    t1 = time.time()
    G = build_G(tagged, lambda w, v: 1, mod=p, max_cost=1)
    r = count_partitions(G, mod=p, verbose=True, max_cost=2)
    res.append([int(x) for x in r])
    print(f"  mod {p}: solutions with 0/1/2 foreign onsets = {res[-1]}  ({time.time()-t1:.0f}s)", flush=True)
    known[p] = res[-1][2]
    json.dump({str(k): v for k, v in known.items()}, open("results/r30_residues.json", "w"))
    del G
out = []
for c in range(3):
    val, M = crt([res[i][c] for i in range(len(res))], PRIMES[:len(res)])
    out.append(val)
print(f"CRT over {len(res)} primes (modulus {M:.3e}, total R(3,0) count 949,086,562,609,181 is below it): "
      f"exactly 0 foreign: {out[0]:,}; exactly 1: {out[1]:,}; exactly 2: {out[2]:,}")
json.dump({"by_foreign_onsets": out, "nprimes": len(res), "residues": res}, open("results/r30_by_cost.json", "w"), indent=1)
print(f"done in {time.time()-t0:.0f}s")
