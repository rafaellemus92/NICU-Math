#!/usr/bin/env python3
"""Long floating-point Taylor jet of Z(t) at fixed (nu, phi), to look at how the coefficients grow.

Same method as float_check.py (rotational form P[u x curl u], alias-free grid G > 2(NMAX+2),
modes outside the exact support max|k_i| <= n+1 zeroed), but to high order and one phase.
--form adv uses -P[(u.grad)u] instead, as a rounding check.

Usage: python3 long_jet.py [--nmax 40] [--phi 0.9710730319801146] [--nu 0 1/28 1/10 1/3 1]
Memory grows with NMAX (about 2 GB at NMAX=40). Writes results/long_jet.json and prints:
  root test |a_n|^(-1/n) (a rough radius estimate if the series converges),
  ratio |a_n/a_(n-1)| (steady growth with n means a divergent series),
  sign pattern, and partial sums S_K(t) with the smallest term |a_K t^K|.
"""
import argparse
import json
import os
import time
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def long_jet(nmax, nu, phi, form='rot'):
    G = 2 * (nmax + 2) + 2
    G += G % 2
    x = np.arange(G) * 2 * np.pi / G
    X, Y, Zg = np.meshgrid(x, x, x, indexing='ij')
    kf = np.fft.fftfreq(G, 1.0 / G)
    kr = np.fft.rfftfreq(G, 1.0 / G)
    KX, KY, KZ = np.meshgrid(kf, kf, kr, indexing='ij')
    K = np.array([KX, KY, KZ])
    K2 = KX ** 2 + KY ** 2 + KZ ** 2
    K2s = np.where(K2 == 0, 1, K2)
    KM = np.maximum(np.maximum(abs(KX), abs(KY)), abs(KZ))

    def fft(v): return np.array([np.fft.rfftn(c) for c in v])
    def ifft(v): return np.array([np.fft.irfftn(c, s=(G, G, G), axes=(0, 1, 2)) for c in v])

    def proj(vh):
        d = (K * vh).sum(0) / K2s
        out = vh - K * d
        out[:, K2 == 0] = 0
        return out

    def curlh(vh):
        return 1j * np.array([K[1] * vh[2] - K[2] * vh[1], K[2] * vh[0] - K[0] * vh[2], K[0] * vh[1] - K[1] * vh[0]])

    def gradh(ch):
        return 1j * K * ch

    u0 = np.array([np.sin(Y), np.sin(Zg), np.cos(X) - np.cos(X + Y + phi)])
    Uh = [fft(u0)]
    Up = [u0]
    Wp = [ifft(curlh(Uh[0]))]
    Gp = [np.array([ifft(gradh(Uh[0][i])) for i in range(3)])] if form == 'adv' else None
    for n in range(nmax):
        acc = np.zeros_like(u0)
        if form == 'rot':
            for j in range(n + 1):
                acc += np.cross(Up[j], Wp[n - j], axis=0)
            nh = proj(fft(acc))
        else:
            for j in range(n + 1):
                acc += np.einsum('lxyz,ilxyz->ixyz', Up[j], Gp[n - j])
            nh = -proj(fft(acc))
        nh = nh - nu * K2 * Uh[n]
        Unew = nh / (n + 1) * (KM <= n + 2)
        Uh.append(Unew); Up.append(ifft(Unew)); Wp.append(ifft(curlh(Unew)))
        if form == 'adv':
            Gp.append(np.array([ifft(gradh(Unew[i])) for i in range(3)]))
    z = [float(0.5 * sum(np.mean((Wp[j] * Wp[n - j]).sum(0)) for j in range(n + 1))) for n in range(nmax + 1)]
    return z, G


def exact_z(nu, phi, nmax):
    """[t^n]Z from results/series.json at this (nu, phi), n <= min(nmax, 14)."""
    S = json.load(open(os.path.join(HERE, 'results', 'series.json')))
    out = []
    for n in range(min(nmax, max(int(k) for k in S['orders'])) + 1):
        tot = 0.0
        for m, p in S['orders'][str(n)].items():
            tot += float(sum(Fraction(c) * nu ** d for d, c in enumerate(p))) * np.cos(int(m) * phi)
        out.append(tot)
    return out


def report(z, label, ex):
    n_hi = len(z) - 1
    picks = [n for n in (10, 15, 20, 25, 30, 35, 40) if n <= n_hi]
    print(f'\n{label}')
    print(f'  vs exact series.json, n <= {len(ex) - 1}: max relative difference '
          f'{max(abs(z[n] - ex[n]) / abs(ex[n]) for n in range(len(ex)) if ex[n] != 0):.1e}')
    print('  root test |a_n|^(-1/n): ' + '  '.join(f'n={n}: {abs(z[n]) ** (-1 / n):.3f}' for n in picks))
    print('  ratio |a_n/a_(n-1)|:    ' + '  '.join(f'n={n}: {abs(z[n] / z[n - 1]):.3f}' for n in picks if n >= 20))
    print(f'  sign pattern n=15..{n_hi}: ' + ''.join('+' if z[n] > 0 else '-' for n in range(15, n_hi + 1)))
    for t in (0.5, 1.0, 1.5, 2.0, 4.0):
        S = [sum(z[k] * t ** k for k in range(K + 1)) for K in range(n_hi + 1)]
        kmin = min(range(5, n_hi + 1), key=lambda k: abs(z[k] * t ** k))
        print(f'  t={t}: S_14={S[14]:+.6e}  S_{kmin}={S[kmin]:+.6e} (smallest term |a_K t^K| = {abs(z[kmin] * t ** kmin):.1e} at K={kmin})'
              f'  S_{n_hi}={S[n_hi]:+.3e}  range of S_K for K=14..{n_hi}: {max(S[14:]) - min(S[14:]):.1e}')


def main():
    ap = argparse.ArgumentParser(description='Long float jet of Z(t) at fixed nu and phi')
    ap.add_argument('--nmax', type=int, default=40)
    ap.add_argument('--phi', type=float, default=0.9710730319801146)
    ap.add_argument('--nu', nargs='+', default=['0', '1/28', '1/10', '1/3', '1'])
    ap.add_argument('--form', default='rot', choices=['rot', 'adv'])
    ap.add_argument('--out', default=os.path.join(HERE, 'results', 'long_jet.json'))
    a = ap.parse_args()
    rows = []
    for s in a.nu:
        t0 = time.time()
        z, G = long_jet(a.nmax, float(Fraction(s)), a.phi, a.form)
        rows.append({'nu': s, 'phi': a.phi, 'form': a.form, 'grid': G, 'z': z, 'sec': round(time.time() - t0, 1)})
        report(z, f'nu={s} phi={a.phi} form={a.form} grid={G}^3 ({time.time() - t0:.0f}s)',
               exact_z(Fraction(s), a.phi, a.nmax))
    with open(a.out, 'w') as f:
        json.dump(rows, f, indent=1)
    print('\nwrote', os.path.relpath(a.out))


if __name__ == '__main__':
    main()
