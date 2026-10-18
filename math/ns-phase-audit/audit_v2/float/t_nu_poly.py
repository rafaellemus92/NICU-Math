"""T3 / nu-structure.
(a) Exact nu-polynomial of every c_{n,m} (unit amplitudes) from complex-nu
    sampling nu = r e^{2 pi i l/L}, L=16, r=1/2, combined with M=32 phase DFT,
    N=28, nmax=12.  [t^n]Z has nu-degree <= n (one nu per recurrence step), so
    L=16 > 12 is alias-free, and degrees 13..15 are provably zero (noise floor).
(b) Real-nu least-squares fits of c_{7,2}(nu), c_{10,3}(nu), c_{6,2}, c_{9,3},
    c_{12,4}, c_{8,2} at 9 real nu values."""
import time, numpy as np
from nsseries import Grid, phi_scan, param_scan, laurent
g = Grid(28)
nmax = 12
import os, sys
if os.path.exists("nu_poly.npz") and "--recompute" not in sys.argv:
    d = np.load("nu_poly.npz"); a, mm = d["a"], d["mm"]
else:
    t = time.time()
    a, mm = param_scan("nu", 16, 0.5, 32, nmax, g)
    print("complex-nu scan time", time.time() - t, flush=True)
    np.savez("nu_poly.npz", a=a, mm=mm)
def A(n, e, m):
    return a[n, e, int(np.where(mm == m)[0][0])]
# noise floor: e > n (provably zero), scaled back by r^e
noise = max(abs(A(n, e, m)) * 0.5 ** e for n in range(nmax + 1) for e in range(n + 1, 16) for m in mm)
print("noise floor on r^e*a (provably-zero e>n entries):", noise)
thr = 1e-12
print("\nnu-degrees e present (|a_e r^e| > %.0e) for each (n,m), m=0..4:" % thr)
for n in range(nmax + 1):
    row = []
    for m in range(0, 5):
        es = [e for e in range(16) if abs(A(n, e, m)) * 0.5 ** e > thr]
        row.append(f"m={m}:{es}")
    print(f"n={n:2d}  " + "  ".join(row))
# parity check e == n - m mod 2 and d+e=n+2 (d>=3|m|+2 for |m|>=2 implies e<=n-3|m|)
viol = []
for n in range(nmax + 1):
    for m in range(-(n + 2), n + 3):
        for e in range(16):
            v = abs(A(n, e, m)) * 0.5 ** e
            if v > thr and ((e - (n - m)) % 2 != 0):
                viol.append(("parity", n, m, e, v))
            if v > thr and abs(m) >= 2 and e > n - 3 * abs(m):
                viol.append(("e<=n-3|m|", n, m, e, v))
            if v > thr and abs(m) == 1 and e > n - 1:
                viol.append(("e<=n-1 for |m|=1 (d>=3)", n, m, e, v))
            if v > thr and m == 0 and e > n:
                viol.append(("e<=n for m=0 (d>=2)", n, m, e, v))
print("\nviolations of parity e=n-m (mod 2) and e <= n+2-d_min(m):", viol if viol else "none")
print("\nexact-in-nu coefficients of interest (a_e):")
for (n, m) in [(6, 2), (7, 2), (8, 2), (9, 2), (9, 3), (10, 3), (11, 3), (12, 4)]:
    print(f" c_{{{n},{m}}}(nu) = " + " + ".join(f"({A(n,e,m).real:+.12e})nu^{e}" for e in range(16) if abs(A(n, e, m)) * 0.5 ** e > thr),
          f"   [max |Im|={max(abs(A(n,e,m).imag)*0.5**e for e in range(16)):.1e}]")
print(" c_{7,2} slope vs 207269/14515200 =", 207269/14515200, " rel diff:", (A(7,1,2).real - 207269/14515200)/(207269/14515200))
if "--skip-real" in sys.argv:
    sys.exit(0)
# (b) real-nu fits
nus = np.array([-1/7, -1/14, -1/28, 0.0, 1/56, 1/28, 1/14, 1/7, 1/4])
vals = {k: [] for k in [(6,2),(7,2),(8,2),(9,3),(10,3),(12,4)]}
t = time.time()
for nu in nus:
    _, c, mmr, _ = phi_scan(32, nmax, g, nu=nu)
    for k in vals:
        vals[k].append(laurent(c, mmr, *k).real)
print("\nreal-nu scan time", time.time() - t)
print("real-nu values:")
print("nu: " + " ".join(f"{x:+.6f}" for x in nus))
for k, v in vals.items():
    print(f"c_{k}: " + " ".join(f"{x:+.10e}" for x in v))
for k, v in vals.items():
    v = np.array(v)
    for deg in [1, 2, 3, 4]:
        V = np.vander(nus, deg + 1, increasing=True)
        coef, res, *_ = np.linalg.lstsq(V, v, rcond=None)
        resid = np.abs(V @ coef - v).max()
        print(f"fit c_{k} deg {deg}: coeffs(nu^0..)= " + " ".join(f"{x:+.6e}" for x in coef) + f"   max resid {resid:.1e}")
