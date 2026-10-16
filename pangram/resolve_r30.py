"""
Resolve the open case of the lattice: does R(3,0) (English lists + any onset
of <= 3 consonants, 1-2 vowels, English codas) have a solution with exactly
TWO non-English onsets?  (0 and 1 are impossible: task (a) and check_onset3.)

Step 1 - packing lower bound.  Same DP as structure.packing_min_foreign but
onset items are deduplicated by letter SET (order is irrelevant for packing),
with cost 0 if some ordering of the set is an English onset, else 1.
Returns the minimum number of foreign onsets any letter packing needs.
"""
import sys, time
import numpy as np
from core import *
from structure import NSC, INF, ODD

t0 = time.time()
onsets = sorted(set(ONSETS) | set(free_clusters(3)), key=lambda s: (len(s), s))
eo = set(ONSETS)
cost_by_mask = {}
for o in onsets:
    if not o:
        continue
    m = cmask(o)
    c = 0 if o in eo else 1
    cost_by_mask[m] = min(cost_by_mask.get(m, 9), c)
items = [(m, "on", c) for m, c in cost_by_mask.items()] + \
        [(cmask(c), "co", 0) for c in CODAS if c and c[-1] in ODD]
print(f"items: {len(cost_by_mask)} distinct onset letter-sets ({sum(1 for c in cost_by_mask.values() if c == 0)} English), "
      f"{len(items) - len(cost_by_mask)} odd English codas")
MW = 6
dp = np.full((MW + 1, MW + 1, NSC), INF, dtype=np.int8)
dp[0][0][0] = 0
S = np.arange(NSC, dtype=np.int64)
for n, (m, kind, add) in enumerate(items):
    idx = S[(S & m) == 0]
    tgt = idx | m
    new = dp.copy()
    if kind == "on":
        for a in range(MW):
            for c in range(MW + 1):
                new[a + 1][c][tgt] = np.minimum(new[a + 1][c][tgt], dp[a][c][idx] + add)
    else:
        for a in range(MW + 1):
            for c in range(MW):
                new[a][c + 1][tgt] = np.minimum(new[a][c + 1][tgt], dp[a][c][idx] + add)
    dp = new
    if n % 200 == 0:
        print(f"  item {n}/{len(items)} ({time.time()-t0:.0f}s)", flush=True)
best = int(dp[:, :, NSC - 1].min())
print(f"packing lower bound on the number of non-English onsets in R(3,0): {best}   ({time.time()-t0:.0f}s)")
for a in range(MW + 1):
    for c in range(MW + 1):
        if dp[a][c][NSC - 1] == best:
            print(f"  attained with {a} onsets and {c} codas")
