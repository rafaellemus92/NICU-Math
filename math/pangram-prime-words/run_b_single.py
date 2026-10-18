"""
Task (b), part 2: the smallest SINGLE cluster whose addition to the English
lists makes a solution appear.

A solution with exactly one non-English cluster consists of one 'foreign'
word  f + nucleus + e  (or  e + nucleus + f), where e is an English cluster
(possibly empty) and f is an arbitrary string of k distinct consonants, plus
a partition of the remaining letters into English prime words.  The tables
produced by reach.py give, for every vowel subset V' (4 or 5 vowels) and
consonant subset C', the exact number R_{V'}[C'] of English-prime-word
partitions of V' u C'.  So for every candidate (nucleus, e, consonant set
K_f) we look up R for the complement, and for reachable complements we test
every ordering of K_f for primality of the foreign word.

Output: for each k = 1..KMAX, the number of (f, position) choices that yield
at least one solution, the total number of solutions with exactly one foreign
cluster of length k, and witnesses.
usage: python3 run_b_single.py [KMAX]
"""
import itertools, json, sys, time
import numpy as np
from core import *
from engine import crt, PRIMES, NS

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 5
t0 = time.time()
tabs = [np.load(f"results/reach_mod{i}.npz") for i in range(3)]
mods = PRIMES[:3]
VOWEL_BITS = {v: 1 << i for i, v in enumerate(VOWELS)}
FULLC = NS - 1
ONSET_SET, CODA_SET = set(ONSETS), set(CODAS)
english_prime = english_words(prime_only=True)
print(f"tables loaded, {len(english_prime):,} English prime words ({time.time()-t0:.0f}s)")


def Rvec(Vmask):
    """boolean reachability (nonzero in all three residues is impossible to
    fake: R < prod of moduli) and the three residue arrays."""
    key = f"V{Vmask}"
    rs = [t[key] for t in tabs]
    return (rs[0] != 0) | (rs[1] != 0) | (rs[2] != 0), rs


def Rexact(rs, C):
    return crt([int(r[C]) for r in rs], mods)[0]


cons = np.array([CONS_INDEX[c] for c in CONSONANTS])
subsets_by_k = {k: np.array([sum(1 << i for i in comb) for comb in itertools.combinations(range(20), k)], dtype=np.int64)
                for k in range(1, KMAX + 1)}
pow26 = [26 ** i for i in range(12)]

summary = {}
witness_rows = []
for k in range(1, KMAX + 1):
    tk = time.time()
    n_reachable_sets = 0          # (nucleus, e, K_f) with reachable complement
    n_prime_words = 0             # foreign words (ordered) that are prime and whose complement is reachable
    total_solutions = 0           # sum of R over those
    clusters = {}                 # (f, position) -> number of solutions
    for position, elist in (("onset", CODAS), ("coda", ONSETS)):
        # position = where the FOREIGN cluster sits; elist = English clusters on the other side
        for nu in nuclei(2):
            Vf = sum(VOWEL_BITS[v] for v in nu)
            Vp = 63 ^ Vf
            reach, rs = Rvec(Vp)
            for e in elist:
                if set(e) & set(nu):
                    continue
                emask = cmask(e)
                subs = subsets_by_k[k]
                ok = (subs & emask) == 0
                subs = subs[ok]
                comp = FULLC ^ emask ^ subs
                good = subs[reach[comp]]
                n_reachable_sets += len(good)
                if len(good) == 0:
                    continue
                # enumerate orderings of each good consonant set
                for Kf in good:
                    letters = [CONS_LIST[i] for i in range(20) if Kf >> i & 1]
                    C = FULLC ^ emask ^ int(Kf)
                    R = None
                    for perm in itertools.permutations(letters):
                        f = "".join(perm)
                        if position == "onset":
                            w = f + nu + e
                            if f in ONSET_SET:
                                continue
                        else:
                            w = e + nu + f
                            if f in CODA_SET:
                                continue
                        v = value(w)
                        if not is_prime_py(v):
                            continue
                        if R is None:
                            R = Rexact(rs, C)
                        n_prime_words += 1
                        total_solutions += R
                        key = (f, position)
                        clusters[key] = clusters.get(key, 0) + R
                        if len(witness_rows) < 400 and R > 0:
                            witness_rows.append((k, f, position, w, v, Vp, C, R))
    summary[k] = {"reachable_sets": n_reachable_sets, "prime_foreign_words": n_prime_words,
                  "clusters_with_solutions": len(clusters), "total_solutions": total_solutions}
    print(f"k={k}: reachable complements {n_reachable_sets:,}; prime foreign words with reachable complement "
          f"{n_prime_words:,}; distinct (cluster,position) giving solutions {len(clusters):,}; "
          f"total solutions with exactly one foreign cluster of length {k}: {total_solutions:,}  ({time.time()-tk:.0f}s)", flush=True)
    if clusters:
        best = sorted(clusters.items(), key=lambda kv: -kv[1])[:15]
        print("   most productive added clusters:", ", ".join(f"{f}({pos},{n})" for (f, pos), n in best))
        summary[k]["top_clusters"] = [(f, pos, n) for (f, pos), n in best]
        summary[k]["all_clusters"] = sorted([(f, pos, n) for (f, pos), n in clusters.items()])

# exhibit witnesses for the smallest k
shown = 0
for (k, f, position, w, v, Vp, C, R) in witness_rows:
    if shown >= 6:
        break
    full = 0
    for i in range(6):
        if Vp >> i & 1:
            full |= 1 << (ord(VOWELS[i]) - 97)
    for i in range(20):
        if C >> i & 1:
            full |= 1 << (ord(CONS_LIST[i]) - 97)
    sub = [x for x in english_prime if x[2] & ~full == 0]
    sols, _ = exact_cover_c(sub, max_solutions=1, full=full, tag="single")
    assert sols, "table says reachable but no cover found"
    rest = " ".join(sub[i][0].upper() for i in sols[0])
    vals = " / ".join(f"{sub[i][1]:,}" for i in sols[0])
    print(f"\nwitness (k={k}, foreign {position} '{f}' in word {w.upper()}={v:,}; {R:,} completions):")
    print(f"   {w.upper()} {rest}    values: {v:,} / {vals}")
    shown += 1

json.dump({"summary": summary, "witnesses": [list(map(lambda x: int(x) if isinstance(x, (int, np.integer)) else x, r)) for r in witness_rows[:50]]},
          open("results/b_single_cluster.json", "w"), indent=1)
print(f"done in {time.time()-t0:.0f}s")
