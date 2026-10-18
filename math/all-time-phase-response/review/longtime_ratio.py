"""How long the 'halving b divides the remainder by about 16' check keeps holding.

The package checks R_O(b) = O(u_b) - O(U) - b^2 O2 (O = E, Z, S) only at T = 0.5. This script
runs the same finite system further: ../response.py for U, q1, q2 and the reused
audit_v2/dns/ns.py for the full +-b solves, at a = c = d = 1, nu = 1/28, phi = 0.37,
b = 0.1 and 0.05, RK4 dt = 0.005, on N = 24 (K = 7) and N = 32 (K = 10) grids, to t = 4.
At t = 0.5, 1, 2, 4 it prints the ratios |R_even(0.1)| / |R_even(0.05)| (R_even is the average
over +b and -b) and whether they lie in the package's pre-set window 14..18. As a resolution
indicator it prints the fraction of q2's energy in the outermost retained shell max|k_i| = K.

This is a finite-system check at moderate b. It does not test PROOF.md, whose radius is far
smaller than these b (see radius_ceiling.py).

Run from this folder:  python3 -I -B longtime_ratio.py > longtime_ratio.log
NumPy; about three and a half minutes on one core.
"""
import importlib.util
import platform
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
NU, PHI, DT = 1 / 28, 0.37, 0.005
BS = (0.1, 0.05)
CHECKPOINTS = (0.5, 1.0, 2.0, 4.0)
GRIDS = (24, 32)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(resp, N):
    solver = resp.Response(N, NU)
    full = resp.audit.NS(N, NU)
    Y = solver.initial(PHI)
    states = {(b, s): full.init_family(PHI, b=s * b) for b in BS for s in (1, -1)}
    step, rows = 0, []
    for tc in CHECKPOINTS:
        n = round(tc / DT) - step
        for _ in range(n):
            Y = solver.step(Y, DT)
            for key in states:
                states[key] = full.step(states[key], DT)
        step += n
        Q0, Q2 = solver.quantities(Y[0]), solver.second(Y)
        R = {}
        for b in BS:
            Rp = solver.quantities(states[(b, 1)]) - Q0 - b * b * Q2
            Rm = solver.quantities(states[(b, -1)]) - Q0 - b * b * Q2
            R[b] = 0.5 * (Rp + Rm)
        ratio = np.abs(R[0.1]) / np.abs(R[0.05])
        g = solver.g
        kinf = np.max(np.abs(g.kvec), axis=0)
        e = (g.w * (np.abs(Y[2])**2).sum(axis=0))
        edge = float((e * (kinf == g.K)).sum() / e.sum())
        rows.append({'t': step * DT, 'ratio': ratio, 'Q2': Q2, 'R01_over_b4': R[0.1] / 0.1**4,
                     'edge': edge})
    return rows


def main():
    t_start = time.time()
    print('longtime_ratio.py: remainder ratios |R(0.1)|/|R(0.05)| beyond T = 0.5 (finite systems)')
    print(f'python {platform.python_version()}, numpy {np.__version__}; a = c = d = 1, nu = 1/28, '
          f'phi = {PHI}, dt = {DT}, b = 0.1 and 0.05 (+-b averaged)')
    resp = load('response', PKG / 'response.py')
    allrows = {}
    for N in GRIDS:
        t0 = time.time()
        allrows[N] = run(resp, N)
        print()
        print(f'N = {N} (K = {(N - 1) // 3}), {time.time() - t0:.0f} s')
        print('    t    ratio E    ratio Z    ratio S   max|ratio/16-1|  in 14..18   '
              'S2          R_S(0.1)/b^4   q2 edge-shell energy')
        for r in allrows[N]:
            dev = float(np.max(np.abs(r['ratio'] / 16 - 1)))
            inside = bool(np.all((r['ratio'] > 14) & (r['ratio'] < 18)))
            print(f'  {r["t"]:4.1f}  {r["ratio"][0]:9.4f}  {r["ratio"][1]:9.4f}  {r["ratio"][2]:9.4f}'
                  f'   {100 * dev:8.2f} %       {"yes" if inside else "NO ":<3}       '
                  f'{r["Q2"][2]:+.4e}  {r["R01_over_b4"][2]:+.4e}   {r["edge"]:.1e}')
    print()
    print('N = 24 against N = 32 at each time (relative difference):')
    for r24, r32 in zip(allrows[24], allrows[32]):
        dr = np.max(np.abs(r24['ratio'] - r32['ratio']) / r32['ratio'])
        ds = abs(r24['Q2'][2] - r32['Q2'][2]) / abs(r32['Q2'][2])
        print(f'  t = {r32["t"]:3.1f}: ratios {dr:.1e}, S2 {ds:.1e}')
    print()
    print(f'total wall time {time.time() - t_start:.0f} s')


if __name__ == '__main__':
    main()
