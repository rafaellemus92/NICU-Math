#!/usr/bin/env python3
"""Validation ladder for step1_adaptive.py (see step1_plan.md, section 3).

1. Hilbert transform on a strongly stretched mesh vs. analytic answers.
2. Uniform map reproduces hou_luo.py; a stretched map agrees with it while
   the uniform grid is still resolved.
"""
import sys
import time

import numpy as np

import step1_adaptive as s1
import hou_luo as hl


def test_hilbert(N=4096, L=128.0, r=5e-6):
    print(f"\n[1] Hilbert transform on the stretched mesh, N={N} L={L:g} r={r:g}")
    t0 = time.time()
    g = s1.MeshMap(N, L, r)
    print(f"    mesh built in {time.time() - t0:.1f}s: hmin={g.hmin:.2e} hmax={g.hmax:.2e}"
          f" x(1/2 - 1/N)={g.x[-1]:.15f}  cells/e-fold={N / L:.0f}")
    # map consistency: x(alpha) at the grid from x_at, and the inverse map
    # off-grid points: x_at against a 60-point Gauss-Legendre reference, and the
    # round trip alpha -> x -> alpha
    amid = g.alpha[N // 2:-1] + 0.37 / N
    gx, gw = np.polynomial.legendre.leggauss(60)
    gx, gw = 0.5 * (gx + 1), 0.5 * gw
    aj = g.alpha[N // 2:-1]
    nodes = aj[:, None] + (amid - aj)[:, None] * gx[None, :]
    ref = g.x[N // 2:-1] + (g.rho_at(nodes) * gw[None, :]).sum(axis=1) * (amid - aj)
    err_x = np.max(np.abs(g.x_at(amid) - ref) / np.abs(ref))
    err_a = np.max(np.abs(g.alpha_of(g.x_at(amid)) - amid) * N)
    print(f"    x_at vs 60-pt GL reference (off-grid): max rel err {err_x:.1e};"
          f" round-trip alpha->x->alpha err {err_a:.1e} cells")
    ok = True
    for kk in (1, 3):
        w = np.sin(2 * np.pi * kk * g.x)
        ux, u = g.hilbert_u(w)
        e1 = np.max(np.abs(ux + np.cos(2 * np.pi * kk * g.x)))
        e2 = np.max(np.abs(u + np.sin(2 * np.pi * kk * g.x) / (2 * np.pi * kk)))
        print(f"    sin(2 pi {kk} x): |H err| = {e1:.1e}  |u err| = {e2:.1e}")
        ok &= e1 < 1e-11 and e2 < 1e-12
    for eta in (1e-3, 1e-6):
        th = 2 * np.pi * g.x
        # cosh(eta) - cos(th) written without cancellation for tiny eta, th
        den = 2 * np.sinh(eta / 2) ** 2 + 2 * np.sin(th / 2) ** 2
        w = np.sin(th) / den
        ux, u = g.hilbert_u(w)
        exact = 1.0 - np.sinh(eta) / den
        e1 = np.max(np.abs(ux - exact)) / np.max(np.abs(exact))
        # u exact: integrate u_x: u = x - (1/pi) * atan( coth(eta/2) tan(pi x) )  (mean 0 by oddness)
        u_ex = g.x - np.arctan(np.tan(np.pi * g.x) / np.tanh(eta / 2)) / np.pi
        e2 = np.max(np.abs(u - u_ex)) / np.max(np.abs(u_ex))
        xs = eta / (2 * np.pi)
        tail = g.tail_fraction(np.fft.rfft(w))
        print(f"    spike eta={eta:g} (peak at x*={xs:.1e} = {xs / g.hmin:.0f} cells):"
              f" rel |H err| = {e1:.1e}  rel |u err| = {e2:.1e}  alpha-tail = {tail:.1e}")
        ok &= e1 < 1e-10 and e2 < 1e-10
    print("    PASS" if ok else "    FAIL")
    return ok


def test_vs_baseline(t_end=0.70):
    """Uniform map must reproduce hou_luo.py to round-off. Stretched maps at
    N = 4096 and 8192 are compared with the uniform N = 16384 run (the best
    resolved uniform grid): the difference must shrink fast with N."""
    from scipy.interpolate import CubicSpline
    print(f"\n[2] Against hou_luo.py up to t={t_end}")
    base = hl.run(N=4096, nu=0.0, t_end=t_end, verbose=False)
    uni = s1.run(N=4096, uniform=True, t_end=t_end, wmax_target=1e9, verbose=False)
    n = min(base["t"].size, uni["t"].size)
    dt_err = np.max(np.abs(base["t"][:n] - uni["t"][:n]))
    w_err = np.max(np.abs(base["wmax"][1:n] - uni["wmax_grid"][1:n]) / base["wmax"][1:n])
    print(f"    uniform map N=4096: {uni['steps']} steps vs {base['steps']}; max |t diff| = {dt_err:.1e};"
          f" max rel |max|omega| diff| = {w_err:.1e}  ({uni['seconds']:.1f}s)")
    ok = w_err < 1e-10
    ref = s1.run(N=16384, uniform=True, t_end=t_end, wmax_target=1e9, verbose=False)
    tt = np.linspace(0.2, t_end, 25)
    def cmp(run_):
        out = {}
        for key in ("wmax", "l2w", "l2t"):
            a = CubicSpline(ref["t"], ref[key])(tt)
            b = CubicSpline(run_["t"], run_[key])(tt)
            out[key] = float(np.max(np.abs(a - b) / np.abs(a)))
        return out
    errs = {}
    for N, unif in ((4096, True), (8192, True), (4096, False), (8192, False)):
        st = (s1.run(N=N, uniform=True, t_end=t_end, wmax_target=1e9, verbose=False) if unif
              else s1.run(N=N, L=128.0, r0=0.05, t_end=t_end, wmax_target=1e9, verbose=False))
        errs[(N, unif)] = cmp(st)
        tag = "uniform  " if unif else "stretched"
        print(f"    {tag} N={N}: {st['steps']} steps, tail_max={st['tail_max']:.1e}; max rel diff vs"
              f" uniform N=16384: max|omega| {errs[(N, unif)]['wmax']:.1e}, "
              f"||omega||_2 {errs[(N, unif)]['l2w']:.1e}, ||theta||_2 {errs[(N, unif)]['l2t']:.1e}"
              f"  ({st['seconds']:.1f}s)")
    e4, e8 = errs[(4096, False)], errs[(8192, False)]
    ok &= all(v < 1e-9 for e in (e4, e8) for v in e.values())
    print("    PASS" if ok else "    FAIL")
    return ok


if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2"]
    results = []
    if "1" in which:
        results.append(test_hilbert())
        results.append(test_hilbert(N=8192, L=128.0, r=5e-6))
    if "2" in which:
        results.append(test_vs_baseline())
    print("\nALL PASS" if all(results) else "\nSOME TESTS FAILED")
