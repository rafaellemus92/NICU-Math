"""Fixed-time-step rerun of the 48^3 vs 64^3 field comparison (RESULTS.md section 7).

Runs the package's own solver (periodic_ns_lab_v2/ns_solver.py, from
math/inputs/periodic_ns_lab_v2_audit.zip) at nu = 1/28 and phi = 0.9710730319801146 with
fixed RK4 steps dt = 0.005 (no CFL adaptivity) on 48^3 and 64^3, to T = 2 and T = 4. It prints
Z at each grid and time, then the relative full-field L2 difference after the 48^3 field is
embedded in the 64^3 grid (the package's "L2" column).

usage: python3 fixed_dt_L2.py PKG_DIR [OUT_DIR]      (about 15 min; output: fixed_dt_L2.log)
  PKG_DIR  the unzipped periodic_ns_lab_v2 folder
  OUT_DIR  optional; if given, the final states are saved there as .npy files
"""
import os
import sys

import numpy as np

PKG = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else None
sys.path.insert(0, PKG)
from ns_solver import PeriodicNS  # noqa: E402

PHASE = 0.9710730319801146
DT = 0.005


def run(N):
    s = PeriodicNS(N, 1 / 28)
    u = s.initial(phase=PHASE)
    states = {}
    for T in (2, 4):
        for _ in range(int(round(2.0 / DT))):
            u = s.step(u, DT)
        Z = s.diagnostics(u)['enstrophy']
        print(f'fixed dt{DT} N={N} T={T}: Z = {Z!r}', flush=True)
        states[T] = u
        if OUT:
            np.save(os.path.join(OUT, f'u_N{N}_dt{DT}_fx_T{T}.npy'), u)
    return states


def embed(low, nlo, nhi):
    f = np.rint(np.fft.fftfreq(nlo) * nlo).astype(int)
    idx = f % nhi
    out = np.zeros((3, nhi, nhi, nhi), complex)
    for c in range(3):
        out[c][np.ix_(idx, idx, idx)] = low[c]
    return out


u48 = run(48)
u64 = run(64)
for T in (2, 4):
    d = embed(u48[T], 48, 64) - u64[T]
    rel = np.linalg.norm(d.ravel()) / np.linalg.norm(u64[T].ravel())
    print(f'fixed dt{DT} rel_L2 T={T}: {rel:.6e}')
