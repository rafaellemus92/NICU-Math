"""Exact check of triads.py on the phase family of the main index (section 2.6).

u_phi = (sin y, sin z, cos x - cos(x + y + phi)) on the 2pi-periodic cube has
E = 1, Z = 5/4, D = 7/2 for every phi and S = cos(phi)/4 (proved in Lean in
wyrd-mathlib PhaseFamily.lean).  Here the field is sampled on an N^3 grid, put
through rfftn in the ensemble's convention (coefficients: rfftn(u)/N^3) and
handed to diagnostics(), which must return those numbers to rounding.  The
convention matters: the raw rfftn array would give E = N^6.
Run: python3 test_triads.py
"""
import math, sys
import numpy as np
from triads import diagnostics

N = 24
x = 2 * np.pi * np.arange(N) / N
X, Y, Z3 = np.meshgrid(x, x, x, indexing="ij")
fails = 0
for phi in (0.0, math.pi / 3, 2.0):
    u = np.stack([np.sin(Y), np.sin(Z3), np.cos(X) - np.cos(X + Y + phi)])
    d = diagnostics(np.fft.rfftn(u, axes=(1, 2, 3)) / N ** 3)
    exact = dict(E=1.0, Z=1.25, D=3.5, S=math.cos(phi) / 4)
    err = max(abs(d[k] - exact[k]) for k in exact)
    ok = err < 1e-12
    fails += not ok
    print(("PASS" if ok else "FAIL") + f" phi={phi:.4f}: E={d['E']:.12f} Z={d['Z']:.12f} D={d['D']:.12f} S={d['S']:+.12f} (exact {exact['S']:+.12f}); max error {err:.1e}; sum|c|={d['sum_abs']:.6f} R={d['R']:.6f}")
print("ALL PASS" if not fails else f"{fails} FAILED")
sys.exit(1 if fails else 0)
