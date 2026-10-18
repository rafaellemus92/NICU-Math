#!/usr/bin/env python3
"""Term-by-term checks of the two selection rules, using the leaf-labelled jet (ljet.py).

1. The unpruned labelled jet, summed, reproduces every c[n,m](nu) in results/series.json.
2. Every term of U_n with no b (sin z) leaf is either the single a leaf or linear in the
   (c, d) leaves  (the "passive scalar" lemma, at the level of the velocity).
3. Every Z term with |M| >= 2 has >= 2 b leaves and >= |M| each of a, c, d leaves.
4. Every Z term has L = M (mod 2), L = number of leaves (the parity rule).
5. Sub-models: Z of the reduced flow (no b leaf) has |M| <= 1; Z with a passive phase
   (d never in an advecting slot) has |M| <= 2.

Usage: python3 leaf_check.py [NMAX]    (default 8: a few seconds; NMAX=11 takes several minutes)
"""
import json
import os
import sys
import time

from flint import fmpq, fmpq_poly

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this folder, also under python3 -I
from ljet import jet, zterms, kvec, mof, name

HERE = os.path.dirname(os.path.abspath(__file__))
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
SJ = json.load(open(os.path.join(HERE, 'results', 'series.json')))


def q(s):
    return fmpq(*map(int, s.split('/'))) if '/' in s else fmpq(int(s))


REF = {int(n): {int(m): fmpq_poly([q(a) for a in p]) for m, p in d.items()} for n, d in SJ['orders'].items()}

t0 = time.time()
U = jet(NMAX)
print(f'labelled jet to order {NMAX}: {len(U[-1])} terms in U_{NMAX}, {time.time()-t0:.1f}s')

ok = True
bad = 0
for n, Un in enumerate(U):
    for S, v in Un.items():
        na, nb, nc, nd = S[0] + S[1], S[2] + S[3], S[4] + S[5], S[6] + S[7]
        assert 0 <= n - sum(S) + 1 <= n, (n, S)
        if nb == 0 and not ((nc + nd == 0 and na == 1) or (nc + nd == 1)):
            bad += 1
            print('reduced-sector violation', n, name(S))
print(f'[2] U_n terms with no b leaf are the single a leaf or linear in (c,d): {"PASS" if bad == 0 else "FAIL"}')
ok &= bad == 0

ok3 = ok4 = ok1 = True
for n in range(NMAX + 1):
    harm = {}
    for (j, S1, S2), s in zterms(U, n).items():
        S = tuple(a + b for a, b in zip(S1, S2))
        assert kvec(S) == (0, 0, 0)
        M, L = mof(S), sum(S)
        p = n - (L - 2)
        harm.setdefault(M, {}).setdefault(p, fmpq(0))
        harm[M][p] += s
        na, nb, nc, nd = S[0] + S[1], S[2] + S[3], S[4] + S[5], S[6] + S[7]
        if abs(M) >= 2 and not (nb >= 2 and na >= abs(M) and nc >= abs(M) and nd >= abs(M)):
            ok3 = False
            print('M>=2 term with too few leaves', n, name(S))
        if (L - M) % 2:
            ok4 = False
            print('parity violation', n, name(S))
    polys = {}
    for M, d in harm.items():
        P = fmpq_poly([d.get(i, fmpq(0)) for i in range(max(d) + 1)])
        if not P.is_zero():
            polys[M] = P
    same = polys == REF[n]
    ok1 &= same
    print(f'    n={n:2d}: harmonics {sorted(polys)}  sum of labelled terms == series.json: {same}')
print(f'[1] labelled jet reproduces series.json for n <= {NMAX}: {"PASS" if ok1 else "FAIL"}')
print(f'[3] every |M|>=2 term has >=2 b leaves and >=|M| of each of a, c, d: {"PASS" if ok3 else "FAIL"}')
print(f'[4] every term has L = M mod 2: {"PASS" if ok4 else "FAIL"}')
ok &= ok1 and ok3 and ok4

for label, kw, bound in (('reduced flow (no b leaf)', dict(keep=lambda S: S[2] + S[3] == 0), 1),
                         ('passive phase (d never advects)', dict(passive_d=True), 2)):
    Um = jet(NMAX, **kw)
    seen = set()
    for n in range(NMAX + 1):
        for (j, S1, S2), s in zterms(Um, n).items():
            if s != 0:
                seen.add(mof(tuple(a + b for a, b in zip(S1, S2))))
    good = max(abs(M) for M in seen) <= bound
    ok &= good
    print(f'[5] {label}: harmonics present for n <= {NMAX}: {sorted(seen)}  (|M| <= {bound}: {"PASS" if good else "FAIL"})')

print('ALL', 'PASS' if ok else 'FAIL', f'({time.time()-t0:.1f}s)')
