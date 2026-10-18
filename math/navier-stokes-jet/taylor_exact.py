#!/usr/bin/env python3
"""Exact Taylor jet in time of the enstrophy Z(t) for periodic Navier-Stokes,
with the viscosity nu kept as a symbol.

Problem:  u_t = -P[(u.grad)u] + nu Lap u,  div u = 0,  on the 2pi-periodic cube, no forcing.
Initial data (the phi-family):  u0 = (sin y, sin z, cos x - cos(x+y+phi)).

Taylor recurrence, u = sum_n U_n t^n:
    (n+1) U_{n+1} = nu Lap U_n + sum_j B(U_j, U_{n-j}),   B(a,b) = -P[(a.grad)b].
Every Fourier coefficient of U_n is an exact polynomial in nu with rational coefficients
(python-flint fmpq_poly). Modes are indexed by (kx, ky, kz, m), where m is the power of e^{i phi}.

Output: c[n,m](nu) with  Z = sum_n sum_m c[n,m](nu) t^n e^{i m phi}  (Laurent convention),
and the same for the energy E.  E = (1/2)<|u|^2>, Z = (1/2)<|curl u|^2>, <.> = cube mean.

Storage trick: the exact symmetry u(x;phi) = -u((pi,0,0)-x; -phi) (preserved by NS for every nu)
makes the complex coefficient c(k,m) = R(k,m) when kx is odd and i*R(k,m) when kx is even, with R
real. Only R is stored. The sign factor in conv_into keeps the recurrence closed on real R.
Each order checks: divergence-free, reality, degree in nu <= n, support max|k_i|,|m| <= n+1.

Usage:  python3 taylor_exact.py [NMAX] [--out PATH]
        default NMAX=8, default PATH=results/series_n<NMAX>.json next to this file.
        results/series.json was produced with NMAX=14 (about 12 min on one core).
"""
import argparse
import json
import os
import time

from flint import fmpq, fmpq_poly

HERE = os.path.dirname(os.path.abspath(__file__))
ZERO = fmpq_poly([])
NU = fmpq_poly([0, 1])


def P(c):
    return fmpq_poly([c])


def initial():
    U = {}

    def put(k, i, val):
        v = U.setdefault(k, [ZERO, ZERO, ZERO])
        v[i] = v[i] + P(val)
    # u_x = sin y : c(0,+1,0,0) = -i/2 -> R=-1/2 ; c(0,-1,0,0)=+i/2 -> R=+1/2  (kx even)
    put((0, 1, 0, 0), 0, fmpq(-1, 2)); put((0, -1, 0, 0), 0, fmpq(1, 2))
    # u_y = sin z
    put((0, 0, 1, 0), 1, fmpq(-1, 2)); put((0, 0, -1, 0), 1, fmpq(1, 2))
    # u_z = cos x - cos(x+y+phi)   (kx odd -> R = c)
    put((1, 0, 0, 0), 2, fmpq(1, 2)); put((-1, 0, 0, 0), 2, fmpq(1, 2))
    put((1, 1, 0, 1), 2, fmpq(-1, 2)); put((-1, -1, 0, -1), 2, fmpq(-1, 2))
    return U


def project_scale(acc, factor):
    """acc: dict k -> [p0,p1,p2] unprojected; returns factor*P_k(acc), drops k=0 (asserted zero)."""
    out = {}
    for k, v in acc.items():
        kx, ky, kz, m = k
        k2 = kx * kx + ky * ky + kz * kz
        if k2 == 0:
            assert all(p.is_zero() for p in v), ('nonzero k=0 forcing', k)
            continue
        d = v[0] * kx + v[1] * ky + v[2] * kz
        if d.is_zero():
            w = v
        else:
            d = d * fmpq(-1, k2)
            w = [v[0] + d * kx, v[1] + d * ky, v[2] + d * kz]
        w = [p * factor for p in w]
        if any(not p.is_zero() for p in w):
            out[k] = w
    return out


def conv_into(acc, Ua_list, Ub_list):
    """acc[k] += sum_{p+q=k} s(p,q) (q . Ra(p)) Rb(q) ; B = -P[acc] handled outside."""
    get = acc.get
    for (px, py, pz, pm, podd, a0, a1, a2) in Ua_list:
        for (qx, qy, qz, qm, qodd, b0, b1, b2, q0, q1, q2) in Ub_list:
            # q . Ra(p)
            d = None
            if qx:
                d = a0 * q0
            if qy:
                t = a1 * q1
                d = t if d is None else d + t
            if qz:
                t = a2 * q2
                d = t if d is None else d + t
            if d is None or d.is_zero():
                continue
            if not (podd and qodd):
                d = -d
            k = (px + qx, py + qy, pz + qz, pm + qm)
            v = get(k)
            if v is None:
                acc[k] = [d * b0, d * b1, d * b2]
            else:
                v[0] += d * b0; v[1] += d * b1; v[2] += d * b2


def as_a_list(U):
    return [(k[0], k[1], k[2], k[3], k[0] & 1, v[0], v[1], v[2]) for k, v in U.items()]


def as_b_list(U):
    return [(k[0], k[1], k[2], k[3], k[0] & 1, v[0], v[1], v[2], P(k[0]), P(k[1]), P(k[2]))
            for k, v in U.items()]


def by_spatial(U):
    d = {}
    for k, v in U.items():
        d.setdefault(k[:3], []).append((k[3], v))
    return d


def inner(Ua, Ub_sp, curl):
    """<a.b>_M (curl=False) or <curl a . curl b>_M (curl=True; a div-free) as dict M -> poly."""
    out = {}
    for k, v in Ua.items():
        kx, ky, kz, m = k
        lst = Ub_sp.get((-kx, -ky, -kz))
        if not lst:
            continue
        w = (kx * kx + ky * ky + kz * kz) if curl else 1
        sg = 1 if (kx & 1) else -1
        f = sg * w
        for (mb, vb) in lst:
            s = (v[0] * vb[0] + v[1] * vb[1] + v[2] * vb[2]) * f
            M = m + mb
            out[M] = out.get(M, ZERO) + s
    return out


def check_symmetries(U, n):
    for k, v in U.items():
        kx, ky, kz, m = k
        # divergence free
        assert (v[0] * kx + v[1] * ky + v[2] * kz).is_zero(), ('div', n, k)
        # reality: R(-k,-m) = +R if kx odd, -R if kx even
        w = U.get((-kx, -ky, -kz, -m))
        assert w is not None, ('reality missing', n, k)
        sg = 1 if (kx & 1) else -1
        for i in range(3):
            assert (w[i] - v[i] * sg).is_zero(), ('reality', n, k)
        for i in range(3):
            assert v[i].degree() <= n, ('deg', n, k)
        assert max(abs(kx), abs(ky), abs(kz), abs(m)) <= n + 1


def polystr(p):
    return [str(c) for c in p.coeffs()]


def compute(nmax, out_path=None, verbose=False):
    """Run the recurrence to order nmax. Returns (Zc, Ec, info) with Zc[n][m] an fmpq_poly in nu.
    If out_path is given, the JSON file is rewritten after every order (a checkpoint)."""
    t0 = time.perf_counter()
    U = [initial()]
    check_symmetries(U[0], 0)
    alist = [as_a_list(U[0])]
    blist = [as_b_list(U[0])]
    sp = [by_spatial(U[0])]
    Zc, Ec = {}, {}
    info = {'timing': {}, 'modes': {0: len(U[0])},
            'entries': {0: sum(sum(1 for p in v if not p.is_zero()) for v in U[0].values())}}

    def zE(n):
        z, e = {}, {}
        for j in range(n + 1):
            for M, p in inner(U[j], sp[n - j], True).items():
                z[M] = z.get(M, ZERO) + p
            for M, p in inner(U[j], sp[n - j], False).items():
                e[M] = e.get(M, ZERO) + p
        z = {M: p * fmpq(1, 2) for M, p in z.items() if not p.is_zero()}
        e = {M: p * fmpq(1, 2) for M, p in e.items() if not p.is_zero()}
        return z, e

    Zc[0], Ec[0] = zE(0)
    if out_path:
        dump(out_path, Zc, Ec, info, False)
    for n in range(0, nmax):
        ts = time.perf_counter()
        # (n+1) U_{n+1} = nu Lap U_n + sum_j B(U_j, U_{n-j}),  B(a,b) = -P[(a.grad)b]
        acc = {}
        for j in range(n + 1):
            conv_into(acc, alist[j], blist[n - j])
        # B contributes -acc; viscous term nu*(-|k|^2) U_n (already div-free; projection harmless)
        for k, v in acc.items():
            acc[k] = [-p for p in v]
        for k, v in U[n].items():
            k2 = k[0] ** 2 + k[1] ** 2 + k[2] ** 2
            f = NU * (-k2)
            w = acc.get(k)
            if w is None:
                acc[k] = [v[0] * f, v[1] * f, v[2] * f]
            else:
                w[0] += v[0] * f; w[1] += v[1] * f; w[2] += v[2] * f
        Un = project_scale(acc, fmpq(1, n + 1))
        check_symmetries(Un, n + 1)
        U.append(Un)
        alist.append(as_a_list(Un)); blist.append(as_b_list(Un)); sp.append(by_spatial(Un))
        Zc[n + 1], Ec[n + 1] = zE(n + 1)
        info['timing'][n + 1] = time.perf_counter() - ts
        info['modes'][n + 1] = len(Un)
        info['entries'][n + 1] = sum(sum(1 for p in v if not p.is_zero()) for v in Un.values())
        if verbose:
            print(f'order {n+1}: modes={len(Un)} entries={info["entries"][n+1]} '
                  f'time={info["timing"][n+1]:.1f}s total={time.perf_counter()-t0:.1f}s', flush=True)
        if out_path:
            dump(out_path, Zc, Ec, info, False)
    if out_path:
        dump(out_path, Zc, Ec, info, True)
    return Zc, Ec, info


def serialize(C):
    return {str(n): {str(M): polystr(C[n][M]) for M in sorted(C[n])} for n in sorted(C)}


def dump(path, Zc, Ec, info, final):
    obj = {
        'convention': 'Z=sum_n sum_m c[n,m](nu) t^n e^{i m phi}',
        'polynomial_convention': 'list [a0,a1,...], a_d = coefficient of nu^d, rationals as strings',
        'normalization': 'E=(1/2)<|u|^2>, Z=(1/2)<|curl u|^2>, <.> = cube mean',
        'orders': serialize(Zc),
        'energy_orders': serialize(Ec),
        'note_energy': '[t^n]E is included through the same order as Z (same U_0..U_n)',
        'seconds_per_order': {str(k): v for k, v in info['timing'].items()},
        'modes_per_order_U_n': {str(k): v for k, v in info['modes'].items()},
        'nonzero_component_entries_U_n': {str(k): v for k, v in info['entries'].items()},
        'complete': final,
        'method': 'exact Taylor recurrence, fmpq_poly in nu, real-representative Fourier coefficients',
    }
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('nmax', nargs='?', type=int, default=8)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(HERE, 'results', f'series_n{a.nmax}.json')
    compute(a.nmax, out_path=out, verbose=True)
    print('wrote', os.path.relpath(out))


if __name__ == '__main__':
    main()
