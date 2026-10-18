"""Enumerate EVERY five-pair prime pangram (not just the first) for each even N.
Uses the encoding/primality helpers from the project's own script."""
import importlib.util, sys, time
spec = importlib.util.spec_from_file_location("cp", sys.argv[1])
cp = importlib.util.module_from_spec(spec); spec.loader.exec_module(cp)
FULL = cp.FULL

def build_allowed(limit, encoder):
    primes, isprime = cp.primes_up_to(limit)
    allowed = {}
    for p in primes:
        if p == 2: continue            # ruled out by parity (two_not_mem)
        w = encoder(p); m = cp.letter_mask(w)
        if m is not None: allowed[p] = (w, m)
    return sorted(allowed), allowed

def all_solutions(target, valid, allowed):
    pairs = []
    for p in valid:
        if 2 * p >= target: break
        q = target - p
        if q not in allowed: continue
        mp, mq = allowed[p][1], allowed[q][1]
        if mp & mq: continue
        pairs.append((p, q, mp | mq))
    cover = 0
    for pr in pairs: cover |= pr[2]
    if len(pairs) < 5 or cover != FULL: return []
    by_letter = [[] for _ in range(26)]
    for i, pr in enumerate(pairs):
        for b in range(26):
            if pr[2] >> b & 1: by_letter[b].append(i)
    sols = []
    def rec(used, chosen):
        if len(chosen) == 5:
            if used == FULL: sols.append([pairs[i] for i in chosen])
            return
        best = None
        for b in range(26):
            if used >> b & 1: continue
            opts = [i for i in by_letter[b] if not pairs[i][2] & used]
            if not opts: return
            if best is None or len(opts) < len(best): best = opts
        if best is None: return   # all 26 letters covered by fewer than 5 pairs
        for i in best: rec(used | pairs[i][2], chosen + [i])
    rec(0, [])
    return sols

def run(name, encoder, lo, hi, show):
    t = time.time()
    valid, allowed = build_allowed(hi, encoder)
    found = []
    for N in range(lo, hi + 1, 2):
        for sol in all_solutions(N, valid, allowed):
            found.append((N, sol))
    print(f"== {name}: even N in [{lo}, {hi}] searched in {time.time()-t:.1f}s; "
          f"{len(found)} solutions at {len(set(N for N,_ in found))} distinct sums")
    for N, sol in found[:show]:
        words = " ".join(f"{allowed[p][0]}+{allowed[q][0]}" for p,q,_ in sol)
        print(f"  N={N}  max prime {max(q for _,q,_ in sol)}  {words}  "
              f"{[(p,q) for p,q,_ in sol]}")
    return found

enc = {"coupled": cp.encode, "plain": cp.encode_plain}[sys.argv[2]]
lo, hi, show = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
found = run(sys.argv[2], enc, lo, hi, show)
if found:
    from collections import Counter
    c = Counter(N for N,_ in found)
    print("  solutions per sum:", sorted(c.items())[:40])
    print("  smallest max-prime over all solutions:", min(max(q for _,q,_ in s) for _,s in found))
