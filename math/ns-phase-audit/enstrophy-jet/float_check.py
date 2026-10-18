#!/usr/bin/env python3
"""Independent floating-point check of the exact series (numpy FFT, rotational form).

Equation:  u_t = P(u x curl u) + nu Lap u,  div u = 0,  on [0,2pi]^3.
Recurrence: (n+1) U_{n+1} = nu Lap U_n + sum_j P(U_j x curl U_{n-j}),
            [t^n] Z = (1/2) sum_j <curl U_j . curl U_{n-j}>.
This uses a different form of the nonlinear term from taylor_exact.py (u x curl u instead of
(u.grad)u), real-space products on an FFT grid, and a fixed numerical nu and phi.

No aliasing: U_n has max_j|k_j| <= n+1 (induction), so the product that builds U_{n+1} has
max_j|k_j| <= n+2. An N-point grid samples it exactly if n+2 <= N/2-1. Modes outside the
support are pure rounding noise; they are zeroed each step, because the viscous factor
nu|k|^2/(n+1) would otherwise amplify them.

The phase harmonics are taken by a DFT over L equally spaced phases. Any term of [t^n]Z has
at most n+2 phase leaves, so |m| <= n+2 and L = 36 resolves every harmonic for n <= 14 without a Nyquist ambiguity.

Usage: python3 float_check.py [--nmax 14] [--grid 32] [--phases 36] [--nu 0 1/28 1/3]
Compares every c[n,m] with results/series.json and prints the worst error per order.
"""
import argparse
import json
import os
import time
import sys
from fractions import Fraction

import numpy as np

# Per-order normalized tolerance, fixed before rerunning the imported check.
# 1e-10 allows accumulated float64 FFT/convolution/cancellation error (historical
# n<=14 maximum 6.5e-13), while rejecting coefficient perturbations of 1e-6.
# This is a numerical regression threshold, not a rigorous error bound.
TOLERANCE = 1e-10


def scaled_error(actual, expected):
    scale = max(float(np.max(np.abs(expected))), np.finfo(float).tiny)
    if not np.all(np.isfinite(actual)) or not np.all(np.isfinite(expected)):
        return float("inf")
    return float(np.max(np.abs(actual - expected)) / scale)


HERE = os.path.dirname(os.path.abspath(__file__))


class Grid:
    def __init__(self, N):
        self.N = N
        x = 2 * np.pi * np.arange(N) / N
        self.X, self.Y, self.Zc = np.meshgrid(x, x, x, indexing="ij")
        k = np.fft.fftfreq(N, 1.0 / N)
        kz = np.fft.rfftfreq(N, 1.0 / N)
        KX, KY, KZ = np.meshgrid(k, k, kz, indexing="ij")
        self.K = np.stack([KX, KY, KZ])
        self.K2 = (self.K ** 2).sum(0)
        self.K2inv = np.where(self.K2 == 0, 0, 1.0 / np.where(self.K2 == 0, 1, self.K2))
        self.kmax = np.maximum(np.maximum(np.abs(KX), np.abs(KY)), np.abs(KZ))

    def fft(self, f):
        return np.fft.rfftn(f, axes=(1, 2, 3))

    def ifft(self, fh):
        return np.fft.irfftn(fh, s=(self.N,) * 3, axes=(1, 2, 3))

    def proj(self, fh):
        kdotf = (self.K * fh).sum(0)
        return fh - self.K * (kdotf * self.K2inv)[None]

    def curl_hat(self, uh):
        K = self.K
        return 1j * np.stack([K[1] * uh[2] - K[2] * uh[1],
                              K[2] * uh[0] - K[0] * uh[2],
                              K[0] * uh[1] - K[1] * uh[0]])

    def u0(self, phi):
        X, Y, Zc = self.X, self.Y, self.Zc
        return np.stack([np.sin(Y), np.sin(Zc), np.cos(X) - np.cos(X + Y + phi)])


def cross(a, b):
    return np.stack([a[1] * b[2] - a[2] * b[1],
                     a[2] * b[0] - a[0] * b[2],
                     a[0] * b[1] - a[1] * b[0]])


def jet(g, nu, phi, nmax):
    """Enstrophy Taylor coefficients Z_0..Z_nmax at fixed (nu, phi)."""
    if nmax + 1 > g.N // 2 - 1:
        raise ValueError(f"grid {g.N} too small for alias-free orders up to {nmax}")
    h = g.proj(g.fft(g.u0(phi)))
    uh, ur, wr = [h], [g.ifft(h)], [g.ifft(g.curl_hat(h))]
    for n in range(nmax):
        S = cross(ur[0], wr[n])
        for j in range(1, n + 1):
            S = S + cross(ur[j], wr[n - j])
        hn = (-nu * g.K2[None] * uh[n] + g.proj(g.fft(S))) / (n + 1)
        hn[:, g.kmax > n + 2] = 0
        uh.append(hn)
        ur.append(g.ifft(hn))
        wr.append(g.ifft(g.curl_hat(hn)))
    Zn = np.zeros(nmax + 1)
    for n in range(nmax + 1):
        Zn[n] = 0.5 * sum((wr[j] * wr[n - j]).sum(0).mean() for j in range(n + 1))
    return Zn


def harmonics(g, nu, nmax, L):
    """c_float[n, m] for m = -L/2+1 .. L/2-1 via a DFT over L phases. Returns (array, m-list)."""
    phis = 2 * np.pi * np.arange(L) / L
    Zs = np.array([jet(g, nu, p, nmax) for p in phis])          # (L, nmax+1)
    ms = list(range(-(L // 2) + 1, L // 2))
    E = np.exp(-1j * np.outer(ms, phis))                         # (len(ms), L)
    C = (E @ Zs) / L                                             # (len(ms), nmax+1)
    return C.T, ms


def exact_value(series, n, m, nu):
    p = series["orders"].get(str(n), {}).get(str(m))
    if p is None:
        return Fraction(0)
    return sum(Fraction(a) * nu ** d for d, a in enumerate(p))


def main():
    ap = argparse.ArgumentParser(description="Float FFT check of results/series.json")
    ap.add_argument("--nmax", type=int, default=14)
    ap.add_argument("--grid", type=int, default=32)
    ap.add_argument("--phases", type=int, default=36)
    ap.add_argument("--nu", nargs="+", default=["0", "1/28", "1/3"])
    ap.add_argument("--series", default=os.path.join(HERE, "results", "series.json"))
    a = ap.parse_args()
    series = json.load(open(a.series))
    nmax = a.nmax
    if nmax < 0 or any(str(n) not in series["orders"] for n in range(nmax + 1)):
        ap.error("series must contain every requested order")
    if a.phases % 2 or a.phases <= 2 * (nmax + 2):
        ap.error("use an even phase count greater than 2*(nmax+2)")
    if any(abs(int(m)) >= a.phases // 2 for n in range(nmax + 1)
           for m in series["orders"][str(n)]):
        ap.error("reference harmonics exceed phase resolution")
    g = Grid(a.grid)
    t0 = time.time()
    print(f"grid {a.grid}^3, {a.phases} phases, orders 0..{nmax}, rotational form, float64")
    print("err = max_m |c_float - c_exact| / S,  zero = max |c_float| / S over m with c_exact = 0,  S = max_m |c_exact|")
    worst = 0.0
    for s in a.nu:
        nu = Fraction(s)
        C, ms = harmonics(g, float(nu), nmax, a.phases)
        print(f"\nnu = {nu}")
        for n in range(nmax + 1):
            ex = np.array([float(exact_value(series, n, m, nu)) for m in ms])
            scale = max(float(np.abs(ex).max()), np.finfo(float).tiny)
            err = scaled_error(C[n], ex)
            zero = np.abs(C[n][ex == 0]).max() / scale if (ex == 0).any() else 0.0
            present = [m for m, v in zip(ms, ex) if v != 0 and m >= 0]
            print(f"  n={n:2d}  harmonics m>=0 {present}  err {err:.1e}  zero {zero:.1e}")
            worst = max(worst, err)
    print(f"\nworst scaled error over all nu and n: {worst:.1e}   ({time.time()-t0:.1f}s)")

    print(f"tolerance {TOLERANCE:.1e}: {'PASS' if worst <= TOLERANCE else 'FAIL'}")
    return 0 if worst <= TOLERANCE else 1


if __name__ == "__main__":
    sys.exit(main())
