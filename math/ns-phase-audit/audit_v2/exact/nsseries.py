#!/usr/bin/env python3
"""
Exact small-time Taylor series of the velocity and enstrophy for unforced 3D
incompressible Navier-Stokes on the 2pi-periodic cube (written from scratch).

    u_t + (u.grad)u = -grad p + nu Lap u,  div u = 0,  <u> = 0
    u(x,0) = (alpha sin y, beta sin z, gamma cos x - delta cos(x+y+phi))

Series u(x,t) = sum_n U_n(x) t^n,  recurrence
    (n+1) U_{n+1} = nu Lap U_n + sum_{j=0}^{n} B(U_j, U_{n-j}),
    B(a,b) = -P[(a.grad) b],  P = Leray projector (I - k k^T/|k|^2 per mode).

Representation
--------------
U_n = sum_K c_{n,K} exp(i(k.x + m phi)),  K = (kx,ky,kz,m)  (phi kept as a
Fourier label m, so every result is an exact Laurent polynomial in e^{i phi}).

Phase lemma (proved in the report, verified exactly by phase_lemma_check.py):
c_{n,K} is REAL when kx is odd and PURELY IMAGINARY when kx is even.  We store
the real 3-vector r with c = r (kx odd) or c = i r (kx even).

Each component of r is a polynomial in nu with exact rational coefficients,
stored as a Python list of Fractions/ints (index = power of nu).  nu is fully
symbolic: no evaluation/interpolation is used.

Only the modes that can ever reach the enstrophy coefficients Z_0..Z_N are
computed (support pruning, see `allowed`): the j-th term of
Z_n = 1/2 sum_j <curl U_j . curl U_{n-j}> pairs spatial k of U_j with -k of
U_{n-j}, and supp U_i lies in the generator ball of radius i+1, so U_j is only
needed at spatial k with rho(k) <= N-j+1, rho(k) = min_m gen_norm(k,m).
The pruning is closed under the recurrence (rho is subadditive).
"""
from fractions import Fraction as Fr
import time

# ---------------------------------------------------------------- utilities

def gen_norm(K):
    """L1 norm of K in the basis g1=(0,1,0,0) [alpha], g2=(0,0,1,0) [beta],
    g3=(1,0,0,0) [gamma], g4=(1,1,0,1) [delta] (unimodular, so unique)."""
    kx, ky, kz, m = K
    return abs(ky - m) + abs(kz) + abs(kx - m) + abs(m)


_rho = {}


def rho(k):
    """min over m of gen_norm((k,m)) = |kz| + max(0,kx,ky) - min(0,kx,ky)."""
    v = _rho.get(k)
    if v is None:
        kx, ky, kz = k
        v = abs(kz) + max(0, kx, ky) - min(0, kx, ky)
        _rho[k] = v
    return v


def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def is_zero_vec(v):
    return not any(x for comp in v for x in comp)


def fstr(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def poly_str(p, var="nu"):
    terms = []
    for e, c in enumerate(p):
        if c:
            if e == 0:
                terms.append(fstr(c))
            elif e == 1:
                terms.append(f"({fstr(c)})*{var}")
            else:
                terms.append(f"({fstr(c)})*{var}^{e}")
    return " + ".join(terms) if terms else "0"


# ---------------------------------------------------------------- initial data

def initial(alpha, beta, gamma, delta):
    a, b, g, d = (Fr(x) for x in (alpha, beta, gamma, delta))
    U0 = {
        # alpha sin y e_x : c(0,+1,0,0) = -i a/2 -> r = -a/2 ; c(0,-1,0,0) = +i a/2 -> r = a/2
        (0, 1, 0, 0): [[-a / 2], [0], [0]],
        (0, -1, 0, 0): [[a / 2], [0], [0]],
        # beta sin z e_y
        (0, 0, 1, 0): [[0], [-b / 2], [0]],
        (0, 0, -1, 0): [[0], [b / 2], [0]],
        # gamma cos x e_z (kx odd: real)
        (1, 0, 0, 0): [[0], [0], [g / 2]],
        (-1, 0, 0, 0): [[0], [0], [g / 2]],
        # -delta cos(x+y+phi) e_z
        (1, 1, 0, 1): [[0], [0], [-d / 2]],
        (-1, -1, 0, -1): [[0], [0], [-d / 2]],
    }
    return {K: v for K, v in U0.items() if not is_zero_vec(v)}


# ---------------------------------------------------------------- recurrence

def accumulate_advection(W, Ua, Ub, ok, plen):
    """W[K] += r-representation of the K-mode of (a.grad) b, a=Ua, b=Ub.
    True coefficient: sum_{P+Q=K} (c_P . iQ) c_Q.  With c = i^{e} r
    (e=1 iff kx even) the phase is i^{1+eP+eQ-eK} = +1 iff kx_P, kx_Q both
    odd, else -1."""
    ub = [(Q, Q[0] & 1, B) for Q, B in Ub.items()]
    for P, A in Ua.items():
        p0, p1, p2, p3 = P
        podd = p0 & 1
        A0, A1, A2 = A
        la = len(A0)
        for Q, qodd, B in ub:
            q0, q1, q2, q3 = Q
            ks = (p0 + q0, p1 + q1, p2 + q2)
            if not ok(ks):
                continue
            s = [q0 * A0[i] + q1 * A1[i] + q2 * A2[i] for i in range(la)]
            nz = [(i, x) for i, x in enumerate(s) if x]
            if not nz:
                continue
            if not (podd and qodd):
                nz = [(i, -x) for i, x in nz]
            K = ks + (p3 + q3,)
            w = W.get(K)
            if w is None:
                w = [[0] * plen, [0] * plen, [0] * plen]
                W[K] = w
            for c in range(3):
                Bc = B[c]
                wc = w[c]
                for l, bv in enumerate(Bc):
                    if bv:
                        for i, x in nz:
                            wc[i + l] += x * bv


def series(alpha, beta, gamma, delta, N, verbose=True, prune=True):
    """Return list U[0..N] (dicts K -> [poly_x, poly_y, poly_z]) restricted to
    the modes needed for Z_0..Z_N (all modes if prune=False)."""
    U = [initial(alpha, beta, gamma, delta)]
    for n in range(1, N + 1):
        t0 = time.time()
        lim = N - n + 1
        if prune:
            ok = lambda ks, lim=lim: rho(ks) <= lim
        else:
            ok = lambda ks: True
        plen = n + 1
        W = {}
        for j in range(n):
            accumulate_advection(W, U[j], U[n - 1 - j], ok, plen)
        new = {}
        inv = Fr(1, n)
        keys = set(W) | {K for K in U[n - 1] if ok(K[:3])}
        for K in keys:
            kx, ky, kz, m = K
            kk = kx * kx + ky * ky + kz * kz
            if kk == 0:
                # mean of (u.grad)u must vanish for every phi-harmonic
                assert K not in W or is_zero_vec(W[K]), ("nonzero mean advection", K)
                continue
            vec = [[0] * plen, [0] * plen, [0] * plen]
            if K in W:
                w = W[K]
                dot = [kx * w[0][i] + ky * w[1][i] + kz * w[2][i] for i in range(plen)]
                kv = (kx, ky, kz)
                for c in range(3):
                    for i in range(plen):
                        # B = -P w = -(w - k (k.w)/|k|^2)
                        vec[c][i] = -(w[c][i] - Fr(kv[c] * dot[i], kk))
            if K in U[n - 1]:
                prev = U[n - 1][K]
                for c in range(3):
                    for i, x in enumerate(prev[c]):
                        if x:
                            vec[c][i + 1] += -kk * x  # nu Lap: shift nu-power by 1
            if is_zero_vec(vec):
                continue
            new[K] = [[x * inv for x in comp] for comp in vec]
        U.append(new)
        if verbose:
            print(f"  U_{n}: {len(new)} modes (pairs filter rho<={lim})  {time.time()-t0:.1f}s", flush=True)
    return U


# ---------------------------------------------------------------- diagnostics

def spatial_index(Ud):
    idx = {}
    for K, v in Ud.items():
        idx.setdefault(K[:3], []).append((K[3], v))
    return idx


def pair_inner(Ua, Ub_idx, kind, maxlen, record=None):
    """<f(Ua) . f(Ub)> as Laurent dict m -> poly in nu,
    kind='curl': f = curl,  kind='vel': f = identity.
    <f g> = sum_k f_k . g_{-k}; c_k c'_{-k} = r r' i^{2 e(k)} = (-1)^{e(k)} r r'.
    curl: (ik x a).(-ik x b) = (k x a).(k x b)."""
    out = {}
    for K, A in Ua.items():
        k = K[:3]
        mk = (-k[0], -k[1], -k[2])
        lst = Ub_idx.get(mk)
        if not lst:
            continue
        sgn = 1 if (k[0] & 1) else -1
        kx, ky, kz = k
        kk = kx * kx + ky * ky + kz * kz
        la = len(A[0])
        for m2, B in lst:
            lb = len(B[0])
            p = [0] * maxlen
            for i in range(la):
                a0, a1, a2 = A[0][i], A[1][i], A[2][i]
                if not (a0 or a1 or a2):
                    continue
                if kind == 'curl':
                    ca = (ky * a2 - kz * a1, kz * a0 - kx * a2, kx * a1 - ky * a0)
                else:
                    ca = (a0, a1, a2)
                for l in range(lb):
                    b0, b1, b2 = B[0][l], B[1][l], B[2][l]
                    if not (b0 or b1 or b2):
                        continue
                    if kind == 'curl':
                        cb = (ky * b2 - kz * b1, kz * b0 - kx * b2, kx * b1 - ky * b0)
                    else:
                        cb = (b0, b1, b2)
                    p[i + l] += sgn * (ca[0] * cb[0] + ca[1] * cb[1] + ca[2] * cb[2])
            if any(p):
                m = K[3] + m2
                out[m] = padd(out.get(m, [0] * maxlen), p)
                if record is not None:
                    record.append((K, m2, kk, p))
    return out


def laurent_series(U, N, kind='curl'):
    """Z_n (kind='curl') or E_n (kind='vel') for n=0..N:
    X_n = 1/2 sum_j <f U_j . f U_{n-j}>, as dict m -> poly in nu."""
    idx = [spatial_index(Ud) for Ud in U]
    res = []
    for n in range(N + 1):
        tot = {}
        for j in range(n + 1):
            part = pair_inner(U[j], idx[n - j], kind, n + 1)
            for m, p in part.items():
                tot[m] = padd(tot.get(m, [0] * (n + 1)), p)
        tot = {m: [Fr(x) / 2 for x in p] for m, p in tot.items()}
        tot = {m: p for m, p in tot.items() if any(p)}
        res.append(tot)
    return res


def check_divfree(U):
    for n, Ud in enumerate(U):
        for K, v in Ud.items():
            kx, ky, kz, _ = K
            for i in range(len(v[0])):
                assert kx * v[0][i] + ky * v[1][i] + kz * v[2][i] == 0, ("div", n, K)
    return True
