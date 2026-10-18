"""Targeted witness search for an R(3,0) solution with exactly two non-English
onsets: fix one foreign word W1, then solve the complement with the sub-dictionary
(English words + foreign words inside the complement) under budget 1."""
import sys, time, random
from core import *
t0 = time.time()
onsets = sorted(set(ONSETS) | set(free_clusters(3)), key=lambda s: (len(s), s))
words = generate_words(onsets, nuclei(2), CODAS, prime_only=True, with_tags=True)
eo = set(ONSETS)
plain = [(w, v, m) for (w, v, m, o, c) in words]
cost = [0 if o in eo else 1 for (w, v, m, o, c) in words]
foreign = [i for i in range(len(words)) if cost[i]]
pinned = set("jqvxz")
# try first the foreign words whose onset absorbs the most pinned letters
foreign.sort(key=lambda i: (-sum(ch in pinned for ch in words[i][3]), -len(words[i][3])))
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
head, tail = foreign[:20000], foreign[20000:]
rnd.shuffle(head)
order = head + tail
print(f"{len(plain):,} words, {len(foreign):,} foreign-onset words; trying W1 in priority order", flush=True)
tried = 0
for i in order:
    m1 = plain[i][2]
    comp = FULL & ~m1
    sub_idx = [j for j in range(len(plain)) if plain[j][2] & ~comp == 0]
    sub = [plain[j] for j in sub_idx]
    sub_cost = [cost[j] for j in sub_idx]
    sols, nodes = exact_cover_c(sub, max_solutions=1, costs=sub_cost, budget=1, full=comp, tag="w2")
    tried += 1
    if sols:
        rest = [sub[k] for k in sols[0]]
        print(f"FOUND after {tried} W1 candidates ({time.time()-t0:.0f}s):")
        print("  ", plain[i][0].upper(), " ".join(w[0].upper() for w in rest))
        print("   values:", plain[i][1], [w[1] for w in rest])
        print("   foreign onsets:", words[i][3], [words[sub_idx[k]][3] for k in sols[0] if sub_cost[k]])
        break
    if tried % 200 == 0:
        print(f"  tried {tried} ({time.time()-t0:.0f}s)", flush=True)
else:
    print("no witness found over all foreign W1 (this would prove impossibility)")
