# Prime pangram: a Python replica of the kernel search in wyrd/Wyrd/Minimal.lean (`ec`, `cands`),
# run over every even sum N = 1352 .. 4294. Same candidate primes (odd primes below 4295 with a
# repeat-free coupled name), same pair filter (2p < N, joint name repeat-free) and same rule
# (always cover the smallest unused letter). Prints |V|, total search nodes, total candidate
# pairs, the largest per-N node count with its N, and the run time. A "found at" line would
# contradict smallest_pangram_sum.
# Run from this folder: python3 -I smallest_sum_search_cost.py [path/to/coupled_prime26_pangram.py]
# (default: ../../coupled_prime26_pangram.py; standard library only, <1 s)
# Formerly numerics/_raw/measure.py.

import sys, time, os, importlib.util
sys.dont_write_bytecode = True  # do not leave a __pycache__ next to the imported module
_mod =sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', 'coupled_prime26_pangram.py')
_spec = importlib.util.spec_from_file_location('coupled_prime26_pangram', _mod)
_cp = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_cp)
name = _cp.encode
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def codes(n): return [A.index(c) for c in name(n)]
def small_div(n): return any(n % d == 0 for d in range(2, 66) if d < n)
LIM = 4295
V = [n for n in range(2, LIM) if not (n == 2 or len(set(codes(n))) < len(codes(n)) or small_div(n))]
Vs = set(V)
print('|V| =', len(V))
nodes = 0; cand_total = 0; maxnodes = (0, 0)
def ec(C, used, k):
    global nodes
    nodes += 1
    if k == 0: return len(used) == 26
    l = next(i for i in range(26) if i not in used) if len(used) < 26 else None
    if l is None: return False
    for c in C:
        if l in c and all(x not in used for x in c):
            if ec(C, used + c, k - 1): return True
    return False
t = time.time()
for N in range(1352, 4296, 2):
    n0 = nodes
    C = []
    for p in V:
        if 2 * p < N and (N - p) in Vs:
            b = codes(p) + codes(N - p)
            if len(set(b)) == len(b): C.append(b)
    cand_total += len(C)
    r = ec(C, [], 5)
    if r: print('found at', N); break
    maxnodes = max(maxnodes, (nodes - n0, N))
print('nodes', nodes, 'cands', cand_total, 'max', maxnodes, 'time', time.time() - t)
