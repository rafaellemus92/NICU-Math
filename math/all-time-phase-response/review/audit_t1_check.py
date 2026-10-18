"""The package's b^2 response against the lab-v2 audit's finite-beta DNS at T = 1.

AUDIT.md section 4.3 (row "At finite time, the m = 2 harmonic is even in beta and O(beta^2)")
reports c2/beta^2 at T = 1, nu = 1/28, for beta = 0.4, 0.2, 0.1, 0.05, where c2 is the Laurent
(e^(2 i phi)) harmonic of the enstrophy Z(T, phi) of full finite-beta solves. Its source,
../../ns-phase-audit/audit_v2/xcheck/p1_finite_time.log, prints them to 7 digits; the solver is
audit_v2/dns/ns.py at N = 24, dt = 0.01, on the 8 phases 2 pi j/8 + 0.137.

At b = 0 the enstrophy has no m = 2 harmonic (P1), so c2(beta)/beta^2 -> [Z2]_(m=2) as beta -> 0.
This script (i) reads the audit's values from the log and checks that AUDIT.md's table quotes
them, (ii) extrapolates them to beta -> 0 (Richardson in beta^2), and (iii) computes the
Laurent m = 2 coefficient of the package's variational Z2 (../response.py, same ns.py
discretisation, N = 24, dt = 0.01) on the audit's 8 phases and on the package's own 8 phases
2 pi j/8. Both lines use the same spatial discretisation; they differ in method (finite beta
versus the b^2 variational equations).

Run from this folder:  python3 -I -B audit_t1_check.py > audit_t1_check.log
Standard library and NumPy; about one minute on one core.
"""
import importlib.util
import math
import platform
import re
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
AUDIT_DIR = PKG.parent / 'ns-phase-audit' / 'audit_v2'
LOG = AUDIT_DIR / 'xcheck' / 'p1_finite_time.log'
AUDIT_MD = AUDIT_DIR / 'AUDIT.md'
NU, T, DT, N, M = 1 / 28, 1.0, 0.01, 24, 8


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    t_start = time.time()
    print('audit_t1_check.py: package Z2 cos 2phi at T = 1 against AUDIT.md section 4.3')
    print(f'python {platform.python_version()}, numpy {np.__version__}')

    # (i) the audit's finite-beta values
    pat = re.compile(r'beta=([+-]\d+\.\d+): c2=([+-]\d\.\d+e[+-]\d+).*c2/beta\^2=([+-]\d\.\d+e[+-]\d+)')
    audit = {}
    for line in LOG.read_text().splitlines():
        mt = pat.search(line)
        if mt:
            audit[float(mt.group(1))] = float(mt.group(3))
    print()
    print('(i) ns-phase-audit/audit_v2/xcheck/p1_finite_time.log, Laurent c2/beta^2 of Z(T = 1):')
    for b, v in audit.items():
        print(f'    beta = {b:+.2f}: {v:+.6e}')
    row = next(l for l in AUDIT_MD.read_text().splitlines()
               if l.startswith('| At finite time, the m = 2 harmonic'))
    quoted = [float(x.replace('−', '-')) for x in re.findall(r'−1\.\d+e-3', row)]
    expect = [float(f'{audit[b]:.4e}') for b in (0.4, 0.2, 0.1, 0.05)]
    print(f'    AUDIT.md section 4.3 quotes {quoted}; the log rounded to 5 digits gives {expect}')
    assert quoted == expect
    assert audit[-0.1] == audit[0.1]
    print('    beta = -0.1 equals beta = +0.1 (even in beta), as AUDIT.md says')

    # (ii) extrapolation to beta -> 0: f(beta) = A + B beta^2 + C beta^4 + ...
    f = audit
    rich_05 = f[0.05] + (f[0.05] - f[0.1]) / 3
    rich_10 = f[0.1] + (f[0.1] - f[0.2]) / 3
    rich3 = (64 * f[0.05] - 20 * f[0.1] + f[0.2]) / 45
    # the log prints 7 digits: each value is uncertain by half a unit in the last place
    ulp = 5e-10
    round_05 = (4 * ulp + ulp) / 3
    print()
    print('(ii) Extrapolation of c2/beta^2 to beta -> 0:')
    print(f'    Richardson from beta = 0.1, 0.05:          {rich_05:+.7e}   (rounding of the log '
          f'alone allows +-{round_05:.1e})')
    print(f'    Richardson from beta = 0.2, 0.1:           {rich_10:+.7e}')
    print(f'    three-point (0.2, 0.1, 0.05; drops beta^4): {rich3:+.7e}')

    # (iii) the package's variational Z2, Laurent m = 2 at T = 1
    resp = load('response', PKG / 'response.py')
    solver = resp.Response(N, NU)
    steps = round(T / DT)
    t0 = time.time()
    results = {}
    for label, offset in (('audit phases 2 pi j/8 + 0.137', 0.137), ('package phases 2 pi j/8', 0.0)):
        phis = 2 * np.pi * np.arange(M) / M + offset
        z2 = []
        for phi in phis:
            Y = solver.initial(phi)
            for _ in range(steps):
                Y = solver.step(Y, DT)
            z2.append(solver.second(Y)[1])
        c2 = complex(np.mean(np.array(z2) * np.exp(-2j * phis)))
        results[label] = c2
    print()
    print(f'(iii) response.py, N = {N} (K = {(N - 1) // 3}), dt = {DT}, T = {T}, nu = 1/28, '
          f'a = c = d = 1 ({time.time() - t0:.0f} s):')
    for label, c2 in results.items():
        print(f'    {label:<30}: Laurent [Z2]_(m=2) = {c2.real:+.7e} (imaginary part {c2.imag:+.1e}); '
              f'cosine amplitude {2 * c2.real:+.7e}')
    pkg = results['audit phases 2 pi j/8 + 0.137'].real
    print()
    print('Relative differences, package against the audit extrapolations:')
    for name, v in (('Richardson 0.1/0.05', rich_05), ('Richardson 0.2/0.1', rich_10),
                    ('three-point', rich3)):
        print(f'    {name:<20}: {abs(pkg - v) / abs(v):.1e}')
    print(f'    (the 7-digit rounding of the log allows about {round_05 / abs(rich_05):.0e} '
          'relative in the Richardson 0.1/0.05 value)')
    print()
    print(f'total wall time {time.time() - t_start:.0f} s')


if __name__ == '__main__':
    main()
