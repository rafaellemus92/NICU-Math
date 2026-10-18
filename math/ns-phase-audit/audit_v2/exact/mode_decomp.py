#!/usr/bin/env python3
"""Mode decomposition of the Laurent coefficient z_{n,m} (default n=6, m=2, unit
amplitudes, nu symbolic): contributions of each ordered pair (j, n-j) of
1/2 <curl U_j . curl U_{n-j}>, of each |k|^2 shell, and of each wave vector k
(with the split m = m_j + m_{n-j} of the phi-labels).
usage: mode_decomp.py [n] [m] [alpha beta gamma delta]
"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from nsseries import series, spatial_index, pair_inner, poly_str, padd, fstr

n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
mt = int(sys.argv[2]) if len(sys.argv) > 2 else 2
amps = [Fr(x) for x in sys.argv[3:7]] if len(sys.argv) > 6 else [Fr(1)] * 4

U = series(*amps, n, verbose=False, prune=False)
idx = [spatial_index(u) for u in U]
half = Fr(1, 2)
per_j = {}
per_shell = {}
per_k = {}
per_shell_j = {}
for j in range(n + 1):
    rec = []
    pair_inner(U[j], idx[n - j], 'curl', n + 1, record=rec)
    for K, m2, kk, p in rec:
        if K[3] + m2 != mt:
            continue
        p = [half * x for x in p]
        per_j[j] = padd(per_j.get(j, [0] * (n + 1)), p)
        per_shell[kk] = padd(per_shell.get(kk, [0] * (n + 1)), p)
        per_shell_j[(kk, j)] = padd(per_shell_j.get((kk, j), [0] * (n + 1)), p)
        key = (K[:3], j, K[3], m2)
        per_k[key] = padd(per_k.get(key, [0] * (n + 1)), p)

tot = [0] * (n + 1)
for p in per_j.values():
    tot = padd(tot, p)
print(f"z_(n={n}, m={mt}) amps={[str(a) for a in amps]}: total = {poly_str(tot)}")
print("\n-- by ordered pair (j, n-j): 1/2 <curl U_j . curl U_{n-j}>|_{e^{i m phi}} --")
for j in sorted(per_j):
    print(f"  j={j} ({j},{n-j}): {poly_str(per_j[j])}")
print("\n-- by unordered pair {j, n-j} --")
for j in range(0, n // 2 + 1):
    p = padd(per_j.get(j, [0]), per_j.get(n - j, [0])) if j != n - j else per_j.get(j, [0])
    print(f"  {{{j},{n-j}}}: {poly_str(p)}")
print("\n-- by shell |k|^2 (summed over j) --")
for kk in sorted(per_shell):
    print(f"  |k|^2={kk}: {poly_str(per_shell[kk])}")
print("\n-- by shell and ordered pair --")
for (kk, j) in sorted(per_shell_j):
    p = per_shell_j[(kk, j)]
    if any(p):
        print(f"  |k|^2={kk} j={j}: {poly_str(p)}")
print("\n-- by wave vector k (of the U_j factor), j, phi-label split (m_j, m_{n-j}) --")
for key in sorted(per_k, key=lambda t: (sum(x * x for x in t[0]), t[1], t[0], t[2])):
    p = per_k[key]
    if any(p):
        k, j, m1, m2 = key
        print(f"  k={k} |k|^2={sum(x*x for x in k)} j={j} m_j={m1:+d} m_(n-j)={m2:+d}: {poly_str(p)}")
# by +-k combined (spatial wave vector up to sign), summed over j and splits
comb = {}
for (k, j, m1, m2), p in per_k.items():
    kc = max(k, tuple(-x for x in k))
    comb[kc] = padd(comb.get(kc, [0] * (n + 1)), p)
print("\n-- by wave-vector pair +-k (summed over j and splits) --")
for k in sorted(comb, key=lambda t: (sum(x * x for x in t), t)):
    if any(comb[k]):
        print(f"  +-{k} |k|^2={sum(x*x for x in k)}: {poly_str(comb[k])}")
