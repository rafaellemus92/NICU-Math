#!/usr/bin/env python3
"""Leaf/tree decomposition of the first phase harmonics, using ljet.py.

Pruned labelled jets (keep only sub-multisets of a target leaf multiset) give, exactly, the
contribution of that multiset to [t^n]Z, split by pairing (j, n-j), by the leaf content of each
factor, and by whether the phase leaf d ever advects anything ("passive" vs "back-reaction").
Every pruned result is compared with results/series.json.

Usage: python3 decompose.py      (about 3 s; writes results/decompose.log and results/decompose.json)
"""
import json
import os
import sys
import time

from flint import fmpq, fmpq_poly

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this folder, also under python3 -I
from ljet import jet, zterms, kvec, mof, name

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results')
SJ = json.load(open(os.path.join(OUT, 'series.json')))


def q(s):
    return fmpq(*map(int, s.split('/'))) if '/' in s else fmpq(int(s))


REF = {int(n): {int(m): fmpq_poly([q(a) for a in p]) for m, p in d.items()} for n, d in SJ['orders'].items()}
res = {}


def le(S, T):
    return all(a <= b for a, b in zip(S, T))


def multisets(L, M):
    """all 8-count multisets with k=0, phase M, L leaves"""
    out = []

    def rec(pre, left):
        if len(pre) == 7:
            c = tuple(pre + [left])
            if kvec(c) == (0, 0, 0) and mof(c) == M:
                out.append(c)
            return
        for x in range(left + 1):
            rec(pre + [x], left - x)
    rec([], L)
    return out


def tgt(M):
    # (a+,a-,b+,b-,c+,c-,d+,d-) = {d+^M, c-^M, a-^M, b+, b-}
    return (0, M, 1, 1, 0, M, M, 0)


def fl(x):
    return float(x.p) / float(x.q) if hasattr(x, 'p') else float(x)


def sumZ(U, n, M, targets=None):
    tot = fmpq(0)
    parts = {}
    for (j, S1, S2), s in zterms(U, n).items():
        S = tuple(a + b for a, b in zip(S1, S2))
        if mof(S) != M:
            continue
        if targets is not None and S not in targets:
            continue
        tot += s
        parts[(j, S1, S2)] = s
    return tot, parts


lines = []


def out(s=''):
    print(s, flush=True)
    lines.append(s)


T_START = time.time()
# ---------------------------------------------------------------- minimal multisets
out('== Minimal leaf multisets (k=0, phase M) ==')
for M in (1, 2, 3):
    for L in range(2, 3 * M + 3):
        ms = multisets(L, M)
        if ms:
            out(f' M={M}: L={L} -> {len(ms)} multisets: '
                + ', '.join(name(S) for S in ms[:6]) + (' ...' if len(ms) > 6 else ''))
            if M < 2:
                break
            ok = [S for S in ms if (S[2] + S[3]) >= 2]
            if ok:
                out(f'        of these, with >=2 b-leaves (needed for M>=2): ' + ', '.join(name(S) for S in ok[:6]))
                break
for M in (2, 3):
    L = 3 * M + 2
    ms = [S for S in multisets(L, M) if (S[2] + S[3]) >= 2]
    out(f' M={M}: multisets with L={L}, k=0, phase M, nb>=2: {[name(S) for S in ms]}  (unique: {len(ms)==1})')

# ---------------------------------------------------------------- M = 2, target T2
T2 = tgt(2)
t0 = time.time()
U = jet(8, keep=lambda S: le(S, T2))
Up = jet(8, keep=lambda S: le(S, T2), passive_d=True)
out(f'\n== Harmonic 2: target leaf multiset T2 = {name(T2)}  (jet {time.time()-t0:.2f}s) ==')
c62, parts6 = sumZ(U, 6, 2, {T2})
a72, parts7 = sumZ(U, 7, 2, {T2})
g82, parts8g = sumZ(U, 8, 2, {T2})
out(f' [t^6] from T2 : {c62}  (series.json c[6,2] = {REF[6][2]})  equal: {c62 == REF[6][2].coeffs()[0]}')
out(f' [t^7] from T2 : {a72} * nu  (series.json c[7,2] = {REF[7][2]})  equal: {a72 == REF[7][2].coeffs()[1]}')
out(f' [t^8] from T2 : {g82} * nu^2 (series.json gamma = {REF[8][2].coeffs()[2]})  equal: {g82 == REF[8][2].coeffs()[2]}')
res['c62'] = str(c62); res['alpha72'] = str(a72); res['gamma82'] = str(g82)

out('\n -- c[6,2] by pairing (j, 6-j) (ordered; T_j = T_{6-j}) --')
byj = {}
for (j, S1, S2), s in parts6.items():
    byj[j] = byj.get(j, fmpq(0)) + s
for j in range(7):
    v = byj.get(j, fmpq(0))
    out(f'  j={j}: {str(v):>22}  = {fl(v):+.6e}   share {fl(v/c62):+.4f}')
res['c62_by_j'] = {j: str(v) for j, v in byj.items()}
out(' -- unordered: --')
for j in range(4):
    v = byj.get(j, fmpq(0)) + (byj.get(6 - j, fmpq(0)) if j != 3 else 0)
    out(f'  {{{j},{6-j}}}: {str(v):>22} = {fl(v):+.6e}  share {fl(v/c62):+.4f}')

out('\n -- c[6,2] by the leaf content of the lower-order factor (j <= 3; for j<3 doubled to include (6-j, j)) --')
out('    j | leaves of U_j factor        k(U_j)     m | leaves of U_{6-j} factor       |  contribution   share')
rows = []
for (j, S1, S2), s in parts6.items():
    if j > 3:
        continue
    w = s * (2 if j < 3 else 1)
    rows.append((j, S1, S2, w))
rows.sort(key=lambda r: (r[0], -abs(fl(r[3]))))
for j, S1, S2, w in rows:
    out(f'   {j:2d} | {name(S1):26s} {str(kvec(S1)):11s} {mof(S1):+d} | {name(S2):30s} | {fl(w):+.4e}  {fl(w/c62):+.4f}')
res['c62_rows'] = [[j, name(S1), list(kvec(S1)), mof(S1), name(S2), str(w)] for j, S1, S2, w in rows]

out('\n -- c[6,2] by phase carried by each factor --')
cls = {}
for (j, S1, S2), s in parts6.items():
    key = tuple(sorted((mof(S1), mof(S2))))
    cls[key] = cls.get(key, fmpq(0)) + s
for key, v in sorted(cls.items()):
    out(f'  (m1,m2)={key}: {v} = {fl(v):+.6e}  share {fl(v/c62):+.4f}')
res['c62_by_phase_split'] = {str(k): str(v) for k, v in cls.items()}

out('\n -- c[6,2] by location of the two b-leaves --')
cls = {}
for (j, S1, S2), s in parts6.items():
    key = 'same factor' if (S1[2] + S1[3]) in (0, 2) else 'one in each factor'
    cls[key] = cls.get(key, fmpq(0)) + s
for key, v in cls.items():
    out(f'  {key}: {v} = {fl(v):+.6e} share {fl(v/c62):+.4f}')

c62p, parts6p = sumZ(Up, 6, 2, {T2})
a72p, _ = sumZ(Up, 7, 2, {T2})
out('\n -- passive-phase channel: trees in which no d-leaf ever sits in an advecting slot --')
out(f'  c[6,2] passive = {c62p} = {fl(c62p):+.6e} (share {fl(c62p/c62):+.4f}); '
    f'back-reaction (d advects something) = {c62-c62p} = {fl(c62-c62p):+.6e} (share {fl((c62-c62p)/c62):+.4f})')
out(f'  alpha  passive = {a72p} = {fl(a72p):+.6e} (share {fl(a72p/a72):+.4f}); back-reaction = {fl(a72-a72p):+.6e}')
res['c62_passive'] = str(c62p); res['alpha72_passive'] = str(a72p)
byjp = {}
for (j, S1, S2), s in parts6p.items():
    byjp[j] = byjp.get(j, fmpq(0)) + s
out('  passive channel by j: ' + ', '.join(f'j={j}: {fl(v):+.3e}' for j, v in sorted(byjp.items())))

out('\n -- c[7,2] = alpha*nu: by pairing (j, 7-j) --')
byj7 = {}
for (j, S1, S2), s in parts7.items():
    byj7[j] = byj7.get(j, fmpq(0)) + s
for j in range(8):
    v = byj7.get(j, fmpq(0))
    out(f'  j={j}: {fl(v):+.6e}')
lam = -a72 / c62
out(f'  effective first-order damping: c6 t^6 + alpha nu t^7 = c6 t^6 (1 - lambda nu t), '
    f'lambda = -alpha/c6 = {lam} = {fl(lam):.6f}')
res['lambda'] = str(lam)

# dZ/dt = Sigma - 2 nu P (P = palinstrophy (1/2)<|grad omega|^2>), so 7 alpha = sigma_1 - 2 P6
Pz = zterms(U, 6, weight=2)
P6 = sum((s for (j, S1, S2), s in Pz.items() if tuple(a + b for a, b in zip(S1, S2)) == T2), fmpq(0))
sig = 7 * a72 + 2 * P6
out(f'  budget: 7 alpha = sigma_1 - 2 P6, with P6 = [t^6 e^(2i phi)] palinstrophy (nu-free) = {P6} = {fl(P6):+.6e}')
out(f'          direct dissipation -2 P6/7 = {fl(-2*P6/7):+.6e} (share {fl(-2*P6/7/a72):+.4f}); '
    f'viscous change of vortex stretching sigma_1/7 = {fl(sig/7):+.6e} (share {fl(sig/7/a72):+.4f})')
res['P6'] = str(P6); res['sigma1'] = str(sig)
out(f'  gamma (nu^2 part of c[8,2]) = {g82} = {fl(g82):+.6e};  pure-exponential guess c6*lambda^2/2 = {fl(c62*lam*lam/2):+.6e}')

# ---------------------------------------------------------------- beta of c[8,2]: all L=10 multisets
ms10 = multisets(10, 2)
ms10b = [S for S in ms10 if (S[2] + S[3]) >= 2 and S[0] + S[1] >= 2 and S[4] + S[5] >= 2 and S[6] + S[7] >= 2]
out(f'\n== beta = nu^0 part of c[8,2]: L=10 multisets with k=0, M=2: {len(ms10)}, '
    f'of which {len(ms10b)} satisfy the count bounds ==')
for S in ms10b:
    out('   ' + name(S))
t0 = time.time()
U10 = jet(8, keep=lambda S: any(le(S, T) for T in ms10b))
beta, parts8b = sumZ(U10, 8, 2, set(ms10b))
out(f' beta from these = {beta} ; series.json beta = {REF[8][2].coeffs()[0]} ; '
    f'equal: {beta == REF[8][2].coeffs()[0]}  ({time.time()-t0:.1f}s)')
bym = {}
for (j, S1, S2), s in parts8b.items():
    S = tuple(a + b for a, b in zip(S1, S2))
    bym[S] = bym.get(S, fmpq(0)) + s
for S, v in bym.items():
    out(f'   {name(S):40s} {fl(v):+.6e}  share {fl(v/beta):+.4f}')
res['beta82'] = str(beta)
res['beta82_by_multiset'] = {name(S): str(v) for S, v in bym.items()}

# ---------------------------------------------------------------- M = 3, 4 first appearance
for M, n0 in ((3, 9), (4, 12)):
    T = tgt(M)
    t0 = time.time()
    UM = jet(n0 + 1, keep=lambda S, T=T: le(S, T))
    UMp = jet(n0, keep=lambda S, T=T: le(S, T), passive_d=True)
    cM, partsM = sumZ(UM, n0, M, {T})
    aM, _ = sumZ(UM, n0 + 1, M, {T})
    cMp, _ = sumZ(UMp, n0, M, {T})
    refc = REF[n0][M].coeffs()
    refa = REF[n0 + 1][M].coeffs()
    out(f'\n== Harmonic {M}: target {name(T)} ({time.time()-t0:.1f}s) ==')
    out(f' c[{n0},{M}] = {cM} = {fl(cM):+.6e}; series.json {REF[n0][M]}; equal {len(refc)==1 and cM == refc[0]}')
    out(f' c[{n0+1},{M}] = {aM} nu; series.json {REF[n0+1][M]}; equal {len(refa)==2 and aM == refa[1]}')
    out(f' lambda_{M} = -alpha/c = {fl(-aM/cM):.6f}')
    cls = {}
    for (j, S1, S2), s in partsM.items():
        key = tuple(sorted((mof(S1), mof(S2))))
        cls[key] = cls.get(key, fmpq(0)) + s
    out(' by phase split: ' + ', '.join(f'{k}: {fl(v/cM):+.4f}' for k, v in sorted(cls.items())))
    out(f' passive-phase share: {fl(cMp/cM):+.4f}')
    byj = {}
    for (j, S1, S2), s in partsM.items():
        byj[j] = byj.get(j, fmpq(0)) + s
    out(' by pairing j: ' + ', '.join(f'{j}: {fl(v/cM):+.4f}' for j, v in sorted(byj.items())))
    res[f'c{n0}{M}'] = str(cM); res[f'alpha{n0+1}{M}'] = str(aM)

out(f'\ntotal {time.time()-T_START:.1f}s')
open(os.path.join(OUT, 'decompose.log'), 'w').write('\n'.join(lines) + '\n')
json.dump(res, open(os.path.join(OUT, 'decompose.json'), 'w'), indent=1)
