#!/usr/bin/env python3
"""Independent numerical check (float64 pseudo-spectral DNS, RK4, 2/3 dealiasing)
of the exact series.  Integrates NS for M equally spaced phi, records Z(t,phi),
compares (i) Z(t,phi) with the exact truncated series and (ii) the e^{2i phi}
harmonic (1/M) sum_l Z(t,phi_l) e^{-2 i phi_l} with sum_n z_{n,2} t^n.
usage: dns_check.py series.json nu [Ngrid] [dt] [M] [tmax]
"""
import sys, json
import numpy as np
from fractions import Fraction as Fr


def make_solver(Ng, nu):
    k1 = np.fft.fftfreq(Ng, 1.0 / Ng)
    kr = np.fft.rfftfreq(Ng, 1.0 / Ng)
    KX, KY, KZ = np.meshgrid(k1, k1, kr, indexing='ij')
    K = np.array([KX, KY, KZ])
    K2 = KX ** 2 + KY ** 2 + KZ ** 2
    K2i = np.where(K2 == 0, 1.0, K2)
    kmax = Ng // 3
    dealias = (np.abs(KX) <= kmax) & (np.abs(KY) <= kmax) & (np.abs(KZ) <= kmax)

    def fwd(f):
        return np.fft.rfftn(f, axes=(-3, -2, -1))

    def inv(F):
        return np.fft.irfftn(F, s=(Ng, Ng, Ng), axes=(-3, -2, -1))

    def rhs(uh):
        u = inv(uh)
        adv = np.zeros_like(u)
        for j in range(3):
            dj = inv(1j * K[j] * uh)          # d_j u_i, shape (3,...)
            adv += u[j][None] * dj           # (u.grad)u
        ah = fwd(adv) * dealias
        kdota = (K * ah).sum(0) / K2i
        ph = ah - K * kdota[None]            # Leray projection
        return -ph - nu * K2 * uh

    def enstrophy(uh):
        wh = np.array([1j * (K[1] * uh[2] - K[2] * uh[1]),
                       1j * (K[2] * uh[0] - K[0] * uh[2]),
                       1j * (K[0] * uh[1] - K[1] * uh[0])])
        w = inv(wh)
        return 0.5 * np.mean((w ** 2).sum(0))

    return fwd, rhs, enstrophy


def run(Ng, nu, phi, dt, times, amps=(1, 1, 1, 1)):
    fwd, rhs, enstrophy = make_solver(Ng, nu)
    x = 2 * np.pi * np.arange(Ng) / Ng
    X, Y, Zc = np.meshgrid(x, x, x, indexing='ij')
    a, b, g, d = amps
    u = np.array([a * np.sin(Y), b * np.sin(Zc), g * np.cos(X) - d * np.cos(X + Y + phi)])
    uh = fwd(u)
    out = [enstrophy(uh)]
    t = 0.0
    for T in times[1:]:
        nst = int(round((T - t) / dt))
        h = (T - t) / nst
        for _ in range(nst):
            k1 = rhs(uh); k2 = rhs(uh + 0.5 * h * k1); k3 = rhs(uh + 0.5 * h * k2); k4 = rhs(uh + h * k3)
            uh = uh + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t = T
        out.append(enstrophy(uh))
    return np.array(out)


def series_eval(res, nu, phi, t):
    tot = 0.0
    for n, harm in res["Z"].items():
        for m, p in harm.items():
            c = sum(float(Fr(x)) * nu ** e for e, x in enumerate(p))
            tot += c * np.cos(int(m) * phi) * t ** int(n)   # Laurent coeffs are real, z_{-m}=z_m
    return tot


def series_harm(res, nu, mm, t):
    tot = 0.0
    for n, harm in res["Z"].items():
        p = harm.get(str(mm))
        if p:
            tot += sum(float(Fr(x)) * nu ** e for e, x in enumerate(p)) * t ** int(n)
    return tot


def main():
    res = json.load(open(sys.argv[1]))
    nu = float(Fr(sys.argv[2]))
    Ng = int(sys.argv[3]) if len(sys.argv) > 3 else 32
    dt = float(sys.argv[4]) if len(sys.argv) > 4 else 2e-3
    M = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    tmax = float(sys.argv[6]) if len(sys.argv) > 6 else 0.3
    times = np.linspace(0, tmax, 7)
    phis = 2 * np.pi * np.arange(M) / M
    Zt = np.array([run(Ng, nu, ph, dt, times) for ph in phis])   # (M, nt)
    print(f"DNS: N={Ng}^3 nu={nu:.6g} dt={dt} M={M}; series order N={res['N']}")
    print(" t      max_phi|Z_dns - Z_series|   harmonic m=2: DNS            series          rel.diff   | m=1 DNS      series")
    for it, t in enumerate(times):
        zs = np.array([series_eval(res, nu, ph, t) for ph in phis])
        err = np.max(np.abs(Zt[:, it] - zs))
        h2 = np.mean(Zt[:, it] * np.exp(-2j * phis))
        h1 = np.mean(Zt[:, it] * np.exp(-1j * phis))
        s2 = series_harm(res, nu, 2, t)
        s1 = series_harm(res, nu, 1, t)
        rd = abs(h2.real - s2) / abs(s2) if s2 else float('nan')
        print(f" {t:.3f}  {err:.3e}                   {h2.real:+.10e} (im {h2.imag:+.1e}) {s2:+.10e}  {rd:.2e}  | {h1.real:+.8e} {s1:+.8e}")


if __name__ == '__main__':
    main()
