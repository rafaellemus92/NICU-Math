"""
Task (b), part 1: lattice of relaxations.

Family A  R(o,c): onsets = English ONSETS u {any 0..o distinct consonants},
                  codas  = English CODAS  u {any 0..c distinct consonants},
                  nucleus = 1 or 2 vowels (as in the English regime).
          Each word costs (#non-English clusters it uses) in {0,1,2}.
Family B  F(n,m): onset = any 0..n consonants, nucleus = exactly ONE vowel,
                  coda = any 0..m consonants (the task's regime (2) is F(2,2)).

For each regime: prime dictionary size, packing feasibility (structure.py:
can <=6 onsets + <=6 'odd' codas cover the 20 consonants at all?), exact
number of perfect pangrams (engine, CRT over `nprimes` primes), the minimum
number of non-English clusters any solution needs (exact-cover search with a
cost budget) and one witness.

usage: python3 run_b_lattice.py <regime> [<regime> ...] [--nprimes=N] [--nocount] [--minbudget=B] [--nowitness]
       regime names like R(2,0) or F(1,3); 'A' / 'B' expand to the whole family.
"""
import json, re, sys, time
from core import *
from engine import exact_count
from structure import packing_dp, packing_min_foreign, NSC

args = [a for a in sys.argv[1:] if not a.startswith("--")]
nprimes = 3
for a in sys.argv[1:]:
    if a.startswith("--nprimes"):
        nprimes = int(a.split("=")[1])
do_count = "--nocount" not in sys.argv
minbudget = 0
for a in sys.argv[1:]:
    if a.startswith("--minbudget"):
        minbudget = int(a.split("=")[1])   # budgets below this are already excluded (run_b_single.py)
FAMILY_A = ["R(0,0)", "R(1,0)", "R(0,1)", "R(1,1)", "R(2,0)", "R(0,2)", "R(2,1)", "R(1,2)", "R(2,2)", "R(3,0)", "R(0,3)"]
FAMILY_B = ["F(1,1)", "F(2,1)", "F(1,2)", "F(3,0)", "F(0,3)", "F(2,2)", "F(3,1)", "F(1,3)", "F(4,0)", "F(0,4)",
            "F(3,2)", "F(2,3)", "F(4,1)", "F(1,4)", "F(5,0)", "F(0,5)"]
names = []
for a in args:
    names += FAMILY_A if a == "A" else FAMILY_B if a == "B" else [a]
ONSET_SET, CODA_SET = set(ONSETS), set(CODAS)


def regime(name):
    fam, o, c = re.match(r"([RF])\((\d),(\d)\)", name).groups()
    o, c = int(o), int(c)
    if fam == "R":
        onsets = sorted(set(ONSETS) | set(free_clusters(o)), key=lambda s: (len(s), s))
        codas = sorted(set(CODAS) | set(free_clusters(c)), key=lambda s: (len(s), s))
        return onsets, nuclei(2), codas
    return free_clusters(o), nuclei(1), free_clusters(c)


def analyse(name):
    t0 = time.time()
    onsets, nucs, codas = regime(name)
    words = generate_words(onsets, nucs, codas, prime_only=True, with_tags=True)
    costs = [(o not in ONSET_SET) + (c not in CODA_SET) for (_, _, _, o, c) in words]
    plain = [(w, v, m) for (w, v, m, _, _) in words]
    rec = {"regime": name, "n_onsets": len(onsets), "n_codas": len(codas), "n_nuclei": len(nucs), "n_prime": len(plain)}
    print(f"\n=== {name}: {len(plain):,} prime words (onsets {len(onsets)}, nuclei {len(nucs)}, codas {len(codas)}) "
          f"[{time.time()-t0:.0f}s]", flush=True)
    n_items = len(onsets) + len(codas)
    if n_items <= 8000:
        dp = packing_dp(onsets, codas, max_words=6)
        rec["packing_feasible"] = bool((dp[:, NSC - 1] <= 6).any())
        print(f"  packing bound: 20 consonants coverable by <=6 onsets + <=6 odd codas: {rec['packing_feasible']}", flush=True)
    else:
        rec["packing_feasible"] = None      # too many clusters for the packing DP; the count decides
        print("  packing bound: skipped (too many clusters)", flush=True)
    lo = minbudget
    if rec["packing_feasible"] and name.startswith("R") and n_items <= 1500:
        lo = max(lo, packing_min_foreign(onsets, codas, ONSETS, CODAS))
        rec["packing_min_foreign"] = lo
        print(f"  packing lower bound on the number of non-English clusters: {lo}", flush=True)
    found = None
    if "--nowitness" in sys.argv:
        print("  witness search skipped (--nowitness)", flush=True)
    elif rec["packing_feasible"] is not False and name.startswith("F"):
        # free regimes: almost every cluster is non-English, so the foreign-cluster
        # budget is meaningless; just find one witness.
        sols, nodes = exact_cover_c(plain, max_solutions=1, costs=costs, budget=12, tag=name)
        print(f"  witness search: {'solution' if sols else 'none'} ({nodes:,} nodes)", flush=True)
        if sols:
            s = sols[0]
            rec["witness"] = [(words[i][0], words[i][1], words[i][3], words[i][4], costs[i]) for i in s]
            print("  witness:", show(plain, s))
    elif rec["packing_feasible"]:
        for budget in range(lo, 13):
            sols, nodes = exact_cover_c(plain, max_solutions=1, costs=costs, budget=budget, tag=name)
            print(f"  budget {budget} foreign clusters: {'solution' if sols else 'none'} ({nodes:,} nodes)", flush=True)
            if sols:
                found = budget
                s = sols[0]
                rec["witness"] = [(words[i][0], words[i][1], words[i][3], words[i][4], costs[i]) for i in s]
                print("  witness:", show(plain, s))
                print("  foreign clusters:", [x for x in [(o if o not in ONSET_SET else "", c if c not in CODA_SET else "")
                                              for (_, _, o, c, _) in rec["witness"]] if x != ("", "")])
                rec["witness_foreign"] = sum(x[4] for x in rec["witness"])
                break
    if found is not None and found >= 12:
        found = None            # budget search skipped (--minbudget=12): only the witness's count is known
    rec["min_foreign_clusters"] = found
    if do_count:
        if rec["packing_feasible"] is not False:
            cnt, M = exact_count(plain, nprimes=nprimes)
            rec["count"] = cnt[0]
        else:
            rec["count"] = 0          # proved by the packing bound
        print(f"  exact number of perfect pangrams: {rec['count']:,}", flush=True)
    rec["seconds"] = round(time.time() - t0)
    print(f"  ({rec['seconds']}s)", flush=True)
    json.dump(rec, open(f"results/b_lattice/{name}.json", "w"), indent=1)


for n in names:
    analyse(n)
