#!/usr/bin/env python3
"""Leaf-labelled exact Taylor jet for the phi-family (same arithmetic as taylor_exact.py).

u0 = (sin y, sin z, cos x - cos(x+y+phi)) is split into its 8 Fourier leaves
    0:a+ (0,1,0)  1:a- (0,-1,0)   [a = sin y e_x]
    2:b+ (0,0,1)  3:b- (0,0,-1)   [b = sin z e_y]
    4:c+ (1,0,0)  5:c- (-1,0,0)   [c = cos x e_z]
    6:d+ (1,1,0) m=+1  7:d- (-1,-1,0) m=-1   [d = -cos(x+y+phi) e_z]
Every term of U_n is a tree whose leaves are copies of these; the key of a term is the
leaf multiset S (8 counts).  S fixes the wavevector k(S), the phase m(S)=#d+ - #d-, the number of
leaves L(S) and hence the number of B nodes b=L-1 and the power of nu, p = n - L + 1.
So each key carries a single rational 3-vector (real-representative convention of
taylor_exact.py: complex coefficient = R if kx odd, i*R if kx even).

Recurrence: (n+1) U_{n+1} = nu Lap U_n + sum_j B(U_j, U_{n-j}),  B(a,b) = -P[(a.grad) b].
Options: a pruning predicate on S (keep only keys satisfying it; exact for any predicate that is
closed under taking sub-multisets) and 'passive_d' (drop B(x,y) whenever x contains a d leaf).
"""
from flint import fmpq

LEAF_K = [(0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0), (1, 1, 0), (-1, -1, 0)]
LEAF_M = [0, 0, 0, 0, 0, 0, 1, -1]
LEAF_COMP = [0, 0, 1, 1, 2, 2, 2, 2]
LEAF_R = [fmpq(-1, 2), fmpq(1, 2), fmpq(-1, 2), fmpq(1, 2), fmpq(1, 2), fmpq(1, 2), fmpq(-1, 2), fmpq(-1, 2)]
NAMES = ['a+', 'a-', 'b+', 'b-', 'c+', 'c-', 'd+', 'd-']
Z0 = fmpq(0)


def kvec(S):
    return (S[4] - S[5] + S[6] - S[7], S[0] - S[1] + S[6] - S[7], S[2] - S[3])


def mof(S):
    return S[6] - S[7]


def name(S):
    out = []
    for i, c in enumerate(S):
        if c:
            out.append(NAMES[i] + (('^%d' % c) if c > 1 else ''))
    return '{' + ' '.join(out) + '}'


def initial(keep):
    U = {}
    for i in range(8):
        S = tuple(1 if j == i else 0 for j in range(8))
        if not keep(S):
            continue
        v = [Z0, Z0, Z0]
        v[LEAF_COMP[i]] = LEAF_R[i]
        U[S] = v
    return U


def add(S, T):
    return tuple(a + b for a, b in zip(S, T))


def jet(nmax, keep=lambda S: True, passive_d=False, verbose=False):
    U = [initial(keep)]
    for n in range(nmax):
        acc = {}
        for j in range(n + 1):
            A = U[j]; Bd = U[n - j]
            for S1, a in A.items():
                if passive_d and (S1[6] or S1[7]):
                    continue
                for S2, b in Bd.items():
                    S = add(S1, S2)
                    if not keep(S):
                        continue
                    qx, qy, qz = kvec(S2)
                    d = a[0] * qx + a[1] * qy + a[2] * qz
                    if d == 0:
                        continue
                    px = kvec(S1)[0]
                    if not ((px & 1) and (qx & 1)):
                        d = -d
                    v = acc.get(S)
                    if v is None:
                        acc[S] = [d * b[0], d * b[1], d * b[2]]
                    else:
                        v[0] += d * b[0]; v[1] += d * b[1]; v[2] += d * b[2]
        for S in acc:
            acc[S] = [-x for x in acc[S]]
        for S, v in U[n].items():
            kx, ky, kz = kvec(S)
            f = -(kx * kx + ky * ky + kz * kz)
            w = acc.get(S)
            if w is None:
                acc[S] = [v[0] * f, v[1] * f, v[2] * f]
            else:
                w[0] += v[0] * f; w[1] += v[1] * f; w[2] += v[2] * f
        Un = {}
        sc = fmpq(1, n + 1)
        for S, v in acc.items():
            kx, ky, kz = kvec(S)
            k2 = kx * kx + ky * ky + kz * kz
            if k2 == 0:
                assert all(x == 0 for x in v), ('k=0 forcing', S)
                continue
            dd = v[0] * kx + v[1] * ky + v[2] * kz
            if dd != 0:
                dd = dd / k2
                v = [v[0] - dd * kx, v[1] - dd * ky, v[2] - dd * kz]
            v = [x * sc for x in v]
            if any(x != 0 for x in v):
                assert v[0] * kx + v[1] * ky + v[2] * kz == 0
                Un[S] = v
        U.append(Un)
        if verbose:
            print(f'  order {n+1}: {len(Un)} labelled terms', flush=True)
    return U


def zterms(U, n, weight=1):
    """Return dict (j, S1, S2) -> rational contribution to [t^n]Z  (weight=1: enstrophy, |k|^2;
    weight=2: palinstrophy (1/2)<|grad w|^2>, |k|^4; weight=0: energy)."""
    out = {}
    for j in range(n + 1):
        idx = {}
        for S2, b in U[n - j].items():
            idx.setdefault(kvec(S2), []).append((S2, b))
        for S1, a in U[j].items():
            kx, ky, kz = kvec(S1)
            lst = idx.get((-kx, -ky, -kz))
            if not lst:
                continue
            k2 = kx * kx + ky * ky + kz * kz
            sg = 1 if (kx & 1) else -1
            f = fmpq(sg * k2 ** weight, 2)
            for S2, b in lst:
                s = (a[0] * b[0] + a[1] * b[1] + a[2] * b[2]) * f
                if s != 0:
                    out[(j, S1, S2)] = s
    return out
