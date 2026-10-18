#!/usr/bin/env python3
"""Third, independent exact Taylor jet: one fixed rational viscosity, exact complex rationals.

Written separately from taylor_exact.py and shares no code with it. Differences on purpose:
  - rotational form:  u_t = P(u x curl u) + nu Lap u   (taylor_exact.py uses -P[(u.grad)u]);
  - nu is a fixed rational number, not a symbol;
  - full complex Fourier coefficients (pairs of flint.fmpq), no symmetry reduction.
Fourier keys (kx,ky,kz,m): coefficient of e^{i k.x} e^{i m phi}.
    (n+1) U_{n+1} = -nu |k|^2 U_n + P[ sum_j U_j x curl U_{n-j} ]
    [t^n] Z = (1/2) sum_j < curl U_j . curl U_{n-j} >   ->  Laurent coefficients c[n,M]
    [t^n] E = (1/2) sum_j < U_j . U_{n-j} >
Diagnostics recorded each order: divergence-free, reality c(-k,-m) = conj c(k,m),
support max|k_i| <= n+1, zero mean of the projected force.

Usage:  python3 exact_single_nu.py NU NMAX [--out FILE] [--series results/series.json]
  NU like 1/3 or -2/3.  With --series, every c[n,M] is compared exactly with the
  nu-polynomials in that file evaluated at NU.
"""
import argparse
import json
import os
import re
import sys
import time

from flint import fmpq

HERE = os.path.dirname(os.path.abspath(__file__))
Z0 = fmpq(0)


def u0():
    h = fmpq(1, 2)
    U = {}

    def put(key, comp, re, im):
        v = list(U.get(key, [Z0] * 6))
        v[2 * comp] += re
        v[2 * comp + 1] += im
        U[key] = v
    put((0, 1, 0, 0), 0, Z0, -h)    # sin y  in u_x
    put((0, -1, 0, 0), 0, Z0, h)
    put((0, 0, 1, 0), 1, Z0, -h)    # sin z  in u_y
    put((0, 0, -1, 0), 1, Z0, h)
    put((1, 0, 0, 0), 2, h, Z0)     # cos x  in u_z
    put((-1, 0, 0, 0), 2, h, Z0)
    put((1, 1, 0, 1), 2, -h, Z0)    # -cos(x+y+phi) in u_z
    put((-1, -1, 0, -1), 2, -h, Z0)
    return U


def curl(U):
    W = {}
    for (kx, ky, kz, m), v in U.items():
        ar, ai, br, bi, cr, ci = v
        # k x u
        xr = ky * cr - kz * br; xi = ky * ci - kz * bi
        yr = kz * ar - kx * cr; yi = kz * ai - kx * ci
        zr = kx * br - ky * ar; zi = kx * bi - ky * ai
        # times i : (r + i s) i = -s + i r
        W[(kx, ky, kz, m)] = [-xi, xr, -yi, yr, -zi, zr]
    return W


def cross_acc(S, A, W):
    """S[p+q] += A[p] x W[q] (complex 3-vectors)."""
    for (px, py, pz, pm), a in A.items():
        a1r, a1i, a2r, a2i, a3r, a3i = a
        for (qx, qy, qz, qm), w in W.items():
            w1r, w1i, w2r, w2i, w3r, w3i = w
            key = (px + qx, py + qy, pz + qz, pm + qm)
            c1r = (a2r * w3r - a2i * w3i) - (a3r * w2r - a3i * w2i)
            c1i = (a2r * w3i + a2i * w3r) - (a3r * w2i + a3i * w2r)
            c2r = (a3r * w1r - a3i * w1i) - (a1r * w3r - a1i * w3i)
            c2i = (a3r * w1i + a3i * w1r) - (a1r * w3i + a1i * w3r)
            c3r = (a1r * w2r - a1i * w2i) - (a2r * w1r - a2i * w1i)
            c3i = (a1r * w2i + a1i * w2r) - (a2r * w1i + a2i * w1r)
            s = S.get(key)
            if s is None:
                S[key] = [c1r, c1i, c2r, c2i, c3r, c3i]
            else:
                s[0] += c1r; s[1] += c1i; s[2] += c2r; s[3] += c2i; s[4] += c3r; s[5] += c3i


def project(S):
    out = {}
    mean_nonzero = False
    for key, v in S.items():
        kx, ky, kz, m = key
        k2 = kx * kx + ky * ky + kz * kz
        if k2 == 0:
            if any(x != 0 for x in v):
                mean_nonzero = True
            out[key] = list(v)
            continue
        dr = (kx * v[0] + ky * v[2] + kz * v[4]) / k2
        di = (kx * v[1] + ky * v[3] + kz * v[5]) / k2
        w = [v[0] - kx * dr, v[1] - kx * di, v[2] - ky * dr, v[3] - ky * di, v[4] - kz * dr, v[5] - kz * di]
        if any(x != 0 for x in w):
            out[key] = w
    return out, mean_nonzero


def pair_mean(A, B):
    """Laurent coefficients (in e^{i M phi}) of < A . B > (no conjugation): sum_k A(k,m).B(-k,m')."""
    idx = {}
    for (kx, ky, kz, m), v in B.items():
        idx.setdefault((kx, ky, kz), []).append((m, v))
    res = {}
    for (kx, ky, kz, m), a in A.items():
        lst = idx.get((-kx, -ky, -kz))
        if not lst:
            continue
        for (m2, b) in lst:
            M = m + m2
            re = (a[0] * b[0] - a[1] * b[1]) + (a[2] * b[2] - a[3] * b[3]) + (a[4] * b[4] - a[5] * b[5])
            im = (a[0] * b[1] + a[1] * b[0]) + (a[2] * b[3] + a[3] * b[2]) + (a[4] * b[5] + a[5] * b[4])
            r = res.get(M)
            if r is None:
                res[M] = [re, im]
            else:
                r[0] += re; r[1] += im
    return res


def run(nu, nmax, verbose=False):
    t0 = time.time()
    Us = [u0()]
    Ws = [curl(Us[0])]
    diag = {"div_max_nonzero": 0, "reality_violations": 0, "mean_force_nonzero": False,
            "support_violations": 0, "nmodes": [len(Us[0])], "sec": []}
    for n in range(nmax):
        S = {}
        for j in range(n + 1):
            cross_acc(S, Us[j], Ws[n - j])
        PS, mn = project(S)
        diag["mean_force_nonzero"] |= mn
        Un = Us[n]
        new = {}
        inv = fmpq(1, n + 1)
        keys = set(PS) | set(Un)
        for key in keys:
            kx, ky, kz, m = key
            k2 = kx * kx + ky * ky + kz * kz
            a = PS.get(key, [Z0] * 6)
            b = Un.get(key, [Z0] * 6)
            v = [(a[i] - nu * k2 * b[i]) * inv for i in range(6)]
            if any(x != 0 for x in v):
                new[key] = v
        # diagnostics: div-free, reality c(-k,-m)=conj c(k,m), support max|k_i|<=n+2
        for (kx, ky, kz, m), v in new.items():
            dr = kx * v[0] + ky * v[2] + kz * v[4]
            di = kx * v[1] + ky * v[3] + kz * v[5]
            if dr != 0 or di != 0:
                diag["div_max_nonzero"] += 1
            w = new.get((-kx, -ky, -kz, -m))
            if w is None or any(w[2 * c] != v[2 * c] or w[2 * c + 1] != -v[2 * c + 1] for c in range(3)):
                diag["reality_violations"] += 1
            if max(abs(kx), abs(ky), abs(kz)) > n + 2:
                diag["support_violations"] += 1
        Us.append(new)
        Ws.append(curl(new))
        diag["nmodes"].append(len(new))
        diag["sec"].append(round(time.time() - t0, 2))
        if verbose:
            print(f"  nu={nu} order {n+1}: {len(new)} modes, {time.time()-t0:.1f}s", flush=True)
    Zc, Ec = {}, {}
    for n in range(nmax + 1):
        accZ, accE = {}, {}
        for j in range(n + 1):
            for M, (re, im) in pair_mean(Ws[j], Ws[n - j]).items():
                r = accZ.setdefault(M, [Z0, Z0]); r[0] += re; r[1] += im
            for M, (re, im) in pair_mean(Us[j], Us[n - j]).items():
                r = accE.setdefault(M, [Z0, Z0]); r[0] += re; r[1] += im
        Zc[n] = {M: [v[0] / 2, v[1] / 2] for M, v in accZ.items()}
        Ec[n] = {M: [v[0] / 2, v[1] / 2] for M, v in accE.items()}
    return Zc, Ec, diag


def parse_q(s):
    s = s.strip()
    if "/" in s:
        p, q = s.split("/")
        return fmpq(int(p), int(q))
    return fmpq(int(s))


def eval_series(series, n, M, nu):
    """Exact value of the nu-polynomial c[n,M] from a series.json dict at rational nu."""
    p = series["orders"].get(str(n), {}).get(str(M))
    if p is None:
        return fmpq(0)
    tot, x = fmpq(0), fmpq(1)
    for a in p:
        tot += parse_q(a) * x
        x *= nu
    return tot


def compare(Zc, series, nu):
    """Count exact mismatches between this run and series.json (also nonzero imaginary parts)."""
    bad = []
    for n, d in Zc.items():
        if str(n) not in series["orders"]:
            bad.append((n, "missing order"))
            continue
        Ms = set(M for M, v in d.items() if v[0] != 0 or v[1] != 0) | set(int(m) for m in series["orders"][str(n)])
        for M in Ms:
            re, im = d.get(M, [Z0, Z0])
            if im != 0 or re != eval_series(series, n, M, nu):
                bad.append((n, M))
    return bad


def main():
    ap = argparse.ArgumentParser(description="Exact Taylor jet at one rational nu (rotational form).")
    ap.add_argument("nu")
    ap.add_argument("nmax", type=int)
    ap.add_argument("--out", default=None)
    ap.add_argument("--series", default=None, help="series.json to compare against")
    # a leading space stops argparse from reading a negative rational such as -2/3 as an option
    argv = [" " + s if re.fullmatch(r"-\d+(/\d+)?", s) else s for s in sys.argv[1:]]
    a = ap.parse_args(argv)
    a.nu = a.nu.strip()
    nu = parse_q(a.nu)
    t0 = time.time()
    Zc, Ec, diag = run(nu, a.nmax, verbose=True)
    print("diagnostics:", {k: v for k, v in diag.items() if k != "sec"})
    bad = []
    if a.series:
        series = json.load(open(a.series))
        bad = compare(Zc, series, nu)
        top = max(int(n) for n in series["orders"])
        print(f"compared c[n,M] for n <= {min(a.nmax, top)} with {a.series}: "
              f"{len(bad)} mismatches {bad[:10]}")
    if a.out:
        out = {"nu": a.nu, "nmax": a.nmax, "diag": diag,
               "Z": {str(n): {str(M): [str(v[0]), str(v[1])] for M, v in d.items() if v[0] != 0 or v[1] != 0}
                     for n, d in Zc.items()},
               "E": {str(n): {str(M): [str(v[0]), str(v[1])] for M, v in d.items() if v[0] != 0 or v[1] != 0}
                     for n, d in Ec.items()}}
        json.dump(out, open(a.out, "w"), indent=1)
        print("wrote", a.out)
    print(f"total {time.time()-t0:.1f}s")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
