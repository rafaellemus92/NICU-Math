"""Laurent tables c_{n,m} of [t^n]Z at unit amplitudes for nu = 0, 1/28, 1/7.
Two independent discretisations per nu:
  A: N=28 grid, M=32 phases phi_k = 2pi k/32
  B: N=32 grid, M=36 phases phi_k = 0.1234 + 2pi k/36
Both are alias-free for nmax=12 (N >= 2*12+3=27) and resolve harmonics
|m| <= n+2 <= 14 (M >= 29).  Saves tables_float.npz."""
import time, numpy as np
from nsseries import Grid, phi_scan
nmax = 12
nus = {"0": 0.0, "1/28": 1/28, "1/7": 1/7}
gA, gB = Grid(28), Grid(32)
res = {}
for lab, nu in nus.items():
    t = time.time()
    ZA, cA, mmA, EA = phi_scan(32, nmax, gA, nu=nu)
    ZB, cB, mmB, EB = phi_scan(36, nmax, gB, nu=nu, phi0=0.1234)
    print(f"nu={lab}: {time.time()-t:.1f}s", flush=True)
    res[lab] = (ZA, cA, mmA, ZB, cB, mmB)
np.savez("tables_float.npz", **{f"{k}_{n}": v for k, tup in res.items() for n, v in zip(["ZA","cA","mmA","ZB","cB","mmB"], tup)})
