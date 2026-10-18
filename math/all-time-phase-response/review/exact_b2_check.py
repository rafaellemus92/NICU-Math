"""Exact b-interpolated time-Taylor coefficients of E, Z and S for the phase family, and a
comparison of their b^2 part with ../response.py at small t.

u0 = (a sin y, b sin z, c cos x - d cos(x+y+phi)), a = c = d = 1, nu symbolic.

The repository's exact series code (../../ns-phase-audit/audit_v2/exact/nsseries.py, used
unchanged) gives E_n and Z_n through t^ORDER as exact polynomials in nu and Laurent polynomials
in e^(i phi), at one rational b per run. P_n = <|grad curl u|^2>_n comes from the same series,
and S_n = (n+1) Z_(n+1) + nu P_n (from Z' = S - nu P), through t^(ORDER-1).

By the grading of AUDIT.md section 4.2 (P2), the t^n coefficient with nu^e has b-degree at most
n+2-e for E and Z and n+3-e for S. So exact interpolation through ORDER+3 rational b values
recovers each coefficient as a polynomial in b; one further b value is held out as a check.

Printed: (1) evenness in b (every odd b-power coefficient is zero), the held-out check and the
degree bound; (2) the b^2 coefficients at t = 0, (E2, Z2, S2)(0); (3) the low orders of E2, Z2,
S2; (4) the t^6 cos 2phi coefficient of Z2; (5) where |m| >= 2 phase harmonics first appear in
the b^2 and b^4 parts, against the onset orders in ../PROOF.md section 5; (6) the b = 0 part keeps
|m| <= 1; (7) the leading b^4 terms; (8) response.py's E2, Z2, S2 (and the b = 0 values) at
t = 0.02, 0.05, 0.1, phi = 0.37, nu = 1/28 against the exact series, with the size of the last
series term.

Run from this folder:  python3 -I -B exact_b2_check.py > exact_b2_check.log
Standard library and NumPy; about four minutes on one core (the exact series dominates).
"""
import importlib.util
import math
import platform
import time
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
SERIES = PKG.parent / 'ns-phase-audit' / 'audit_v2' / 'exact' / 'nsseries.py'
ORDER = 10                      # E, Z through t^10; S through t^9
PRIMARY = ['0', '1/3', '-1/3', '1/2', '-1/2', '1', '-1', '3/2', '-3/2', '2', '-2', '3', '-3']
HELD_OUT = ['5/2']
NU = Fr(1, 28)
PHI = 0.37
TIMES = [0.02, 0.05, 0.1]
GRID_N, DT = 48, 0.00125        # response.py grid (cutoff K = 15) and time step


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ns = load('nsseries', SERIES)


def pair_gradcurl(Ua, Ub_idx, maxlen):
    """<grad curl Ua : grad curl Ub> as Laurent dict m -> poly in nu (same conventions as
    nsseries.pair_inner: c_k c'_{-k} = (-1)^{e(k)} r r', and grad adds |k|^2)."""
    out = {}
    for K, Avec in Ua.items():
        k = K[:3]
        lst = Ub_idx.get((-k[0], -k[1], -k[2]))
        if not lst:
            continue
        sgn = 1 if (k[0] & 1) else -1
        kx, ky, kz = k
        kk = kx * kx + ky * ky + kz * kz
        for m2, B in lst:
            p = [0] * maxlen
            for i in range(len(Avec[0])):
                a0, a1, a2 = Avec[0][i], Avec[1][i], Avec[2][i]
                if not (a0 or a1 or a2):
                    continue
                ca = (ky * a2 - kz * a1, kz * a0 - kx * a2, kx * a1 - ky * a0)
                for j in range(len(B[0])):
                    b0, b1, b2 = B[0][j], B[1][j], B[2][j]
                    if not (b0 or b1 or b2):
                        continue
                    cb = (ky * b2 - kz * b1, kz * b0 - kx * b2, kx * b1 - ky * b0)
                    p[i + j] += sgn * kk * (ca[0] * cb[0] + ca[1] * cb[1] + ca[2] * cb[2])
            if any(p):
                m = K[3] + m2
                out[m] = ns.padd(out.get(m, [0] * maxlen), p)
    return out


def observables(beta):
    """E_n, Z_n (n <= ORDER) and S_n (n <= ORDER-1) at one rational beta, a = c = d = 1."""
    U = ns.series(Fr(1), beta, Fr(1), Fr(1), ORDER, verbose=False, prune=True)
    ns.check_divfree(U)
    Z = ns.laurent_series(U, ORDER, 'curl')
    E = ns.laurent_series(U, ORDER, 'vel')
    idx = [ns.spatial_index(Ud) for Ud in U]
    S = []
    for n in range(ORDER):
        P = {}
        for j in range(n + 1):
            for m, p in pair_gradcurl(U[j], idx[n - j], n + 1).items():
                P[m] = ns.padd(P.get(m, [0] * (n + 1)), p)
        s = {}
        for m, p in Z[n + 1].items():
            s[m] = ns.padd(s.get(m, []), [(n + 1) * x for x in p])
        for m, p in P.items():
            s[m] = ns.padd(s.get(m, []), [0] + [Fr(x) for x in p])
        S.append({m: p for m, p in s.items() if any(p)})
    for n in range(ORDER):          # energy identity (n+1) E_(n+1) = -2 nu Z_n, exactly
        for m in set(E[n + 1]) | set(Z[n]):
            lhs = [(n + 1) * x for x in E[n + 1].get(m, [])]
            rhs = [0] + [-2 * x for x in Z[n].get(m, [])]
            L = max(len(lhs), len(rhs))
            assert lhs + [0] * (L - len(lhs)) == rhs + [0] * (L - len(rhs)), ('energy', n, m)
    return {'E': E, 'Z': Z, 'S': S}


def interpolate(xs, ys):
    """Exact Newton interpolation, returned in the monomial basis."""
    coef = list(ys)
    for j in range(1, len(xs)):
        for i in range(len(xs) - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (xs[i] - xs[i - j])
    poly = [coef[-1]]
    for i in range(len(xs) - 2, -1, -1):
        new = [Fr(0)] * (len(poly) + 1)
        for d, c in enumerate(poly):
            new[d + 1] += c
            new[d] -= xs[i] * c
        new[0] += coef[i]
        poly = new
    return poly


def peval(poly, x):
    r = Fr(0)
    for c in reversed(poly):
        r = r * x + c
    return r


def fmt_nu(p):
    terms = [(e, c) for e, c in enumerate(p) if c]
    if not terms:
        return '0'
    return ' + '.join(f'({ns.fstr(c)})' + ('' if e == 0 else ' nu' if e == 1 else f' nu^{e}')
                      for e, c in terms)


def fmt_laurent(d):
    """Laurent dict m -> poly in nu, printed as cos(m phi) amplitudes (2 c_m for m > 0)."""
    if not d:
        return '0'
    out = []
    for m in sorted({abs(m) for m in d}):
        p = d.get(m, [])
        if m:
            assert d.get(-m) == p, 'Laurent coefficients must be symmetric in m'
            p = [2 * c for c in p]
        out.append(f'[{fmt_nu(p)}]' + ('' if m == 0 else f' cos({m} phi)'))
    return ' + '.join(out)


def main():
    t_start = time.time()
    print('exact_b2_check.py: exact b-interpolated time-Taylor coefficients of E, Z, S')
    print(f'python {platform.python_version()}, numpy {np.__version__}; series code '
          'ns-phase-audit/audit_v2/exact/nsseries.py (unchanged), order t^%d' % ORDER)
    xs_all = [Fr(b) for b in PRIMARY + HELD_OUT]
    runs = {}
    for b in xs_all:
        t0 = time.time()
        runs[b] = observables(b)
        print(f'  b = {ns.fstr(b):>4}: series done in {time.time() - t0:5.1f} s', flush=True)
    prim = [Fr(b) for b in PRIMARY]
    held = [Fr(b) for b in HELD_OUT]

    # (1) interpolation in b: coeff[X][k][n] = {m: [nu-power coefficients]}
    coeff = {}
    stats = {'coefficients': 0, 'odd_b_power_nonzero': 0, 'held_out_failures': 0,
             'degree_bound_violations': 0}
    for X in ('E', 'Z', 'S'):
        coeff[X] = {}
        cap = 3 if X == 'S' else 2
        for n in range(len(runs[prim[0]][X])):
            keys = {(m, e) for b in xs_all for m, p in runs[b][X][n].items() for e in range(len(p))}
            for (m, e) in sorted(keys):
                def val(b):
                    p = runs[b][X][n].get(m)
                    return Fr(p[e]) if p is not None and e < len(p) else Fr(0)
                poly = interpolate(prim, [val(b) for b in prim])
                stats['coefficients'] += 1
                stats['held_out_failures'] += sum(peval(poly, b) != val(b) for b in held)
                top = max([k for k, c in enumerate(poly) if c] or [0])
                stats['degree_bound_violations'] += top > n + cap - e
                for k, c in enumerate(poly):
                    if c:
                        stats['odd_b_power_nonzero'] += k % 2
                        lst = coeff[X].setdefault(k, {}).setdefault(n, {}).setdefault(m, [])
                        lst += [Fr(0)] * (e + 1 - len(lst))
                        lst[e] = c
    print()
    print('(1) Interpolation in b through %d values (%s), held out %s:'
          % (len(prim), ', '.join(PRIMARY), ', '.join(HELD_OUT)))
    for k, v in stats.items():
        print(f'    {k}: {v}')
    ok = (stats['odd_b_power_nonzero'] == 0 and stats['held_out_failures'] == 0
          and stats['degree_bound_violations'] == 0)
    print('    => every t^n coefficient of E, Z (n <= %d) and S (n <= %d) is exactly even in b,'
          % (ORDER, ORDER - 1))
    print('       for every phase harmonic and power of nu' if ok else '    CHECK FAILED')

    def part(X, k, n):
        return coeff[X].get(k, {}).get(n, {})

    # (2) t = 0 values of the b^2 coefficients
    print()
    print('(2) b^2 coefficients at t = 0 (exact; every nu and phi):')
    for X in ('E', 'Z', 'S'):
        print(f'    {X}2(0) = {fmt_laurent(part(X, 2, 0))}')
    assert part('E', 2, 0) == {0: [Fr(1, 4)]} and part('Z', 2, 0) == {0: [Fr(1, 4)]}
    assert not part('S', 2, 0)

    # (3) low orders
    print()
    print('(3) Low orders of the b^2 coefficients (cos(m phi) amplitudes, nu symbolic):')
    for X, nmax in (('E', 3), ('Z', 3), ('S', 2)):
        for n in range(nmax + 1):
            print(f'    [t^{n}] {X}2 = {fmt_laurent(part(X, 2, n))}')

    # (4) t^6 cos 2phi of Z2
    c62 = part('Z', 2, 6).get(2, [])
    print()
    print(f'(4) [t^6] cos 2phi of Z2 = {fmt_nu([2 * c for c in c62])}'
          f'   (expected -6487/1555200, no nu terms)')
    assert [2 * c for c in c62] == [Fr(-6487, 1555200)]

    # (5) onset of |m| >= 2 harmonics in the b^(2j) parts
    print()
    print('(5) First order at which a |m| >= 2 harmonic appears in the b^(2j) part; the rule of')
    print('    PROOF.md section 5 is n >= 3|m| + 2(j-1) for Z, 3|m| - 1 + 2(j-1) for S and')
    print('    3|m| + 1 + 2(j-1) for E (E only through a factor nu):')
    shift = {'Z': 0, 'S': -1, 'E': 1}
    violations = 0
    for X in ('Z', 'S', 'E'):
        nmax = max(coeff[X][0])
        for k in sorted(coeff[X]):
            if k == 0:
                continue
            j = k // 2
            for m in range(2, 5):
                rule = 3 * m + shift[X] + 2 * (j - 1)
                orders = [n for n in sorted(coeff[X][k])
                          if any(abs(mm) == m and any(p) for mm, p in coeff[X][k][n].items())]
                violations += sum(n < rule for n in orders)
                if rule <= nmax:
                    first = orders[0] if orders else None
                    note = ''
                    if X == 'E' and first is not None:
                        lead = coeff[X][k][first].get(m, [])
                        note = ', with no nu^0 term' if not lead[0] else ', HAS a nu^0 term'
                    print(f'    {X}: b^{k}, |m| = {m}: rule allows t^{rule} and later; first seen at '
                          f't^{first}{note}')
    print(f'    violations of the rule within the computed orders: {violations}')
    assert violations == 0

    # (6) b = 0 part keeps |m| <= 1
    mmax0 = max(abs(m) for X in ('E', 'Z', 'S') for n in coeff[X][0] for m in coeff[X][0][n])
    print()
    print(f'(6) b^0 part: largest phase harmonic |m| in E, Z, S at any computed order = {mmax0}')
    assert mmax0 <= 1

    # (7) leading b^4 terms
    print()
    print('(7) Leading b^4 terms (first nonzero order; the b^4 remainder is genuinely of order b^4):')
    for X in ('S', 'Z', 'E'):
        n0 = min(coeff[X][4])
        print(f'    [b^4 t^{n0}] {X} = {fmt_laurent(coeff[X][4][n0])}')

    # (8) response.py against the exact series at small t
    def series_value(X, k, t):
        """Partial sum through the last computed order at nu = 1/28, phi = PHI, and the size of
        its last term. The Laurent coefficients are symmetric in m, so the sum is real."""
        nmax = ORDER - 1 if X == 'S' else ORDER
        terms = []
        for n in range(nmax + 1):
            blk = part(X, k, n)
            c = sum(float(sum(cc * NU**e for e, cc in enumerate(p))) * math.cos(m * PHI)
                    for m, p in blk.items())
            terms.append(c * t**n)
        return math.fsum(terms), abs(terms[-1])

    resp = load('response', PKG / 'response.py')
    solver = resp.Response(GRID_N, float(NU))
    Y = solver.initial(PHI)
    tcur = 0.0
    print()
    print(f'(8) response.py (N = {GRID_N}, K = {(GRID_N - 1) // 3}, RK4 dt = {DT}) against the exact '
          f'series, nu = 1/28, phi = {PHI}:')
    print('    quantity     t     response.py               exact series (to t^n)    |diff|    '
          'digits  last term')
    t0 = time.time()
    worst = {}
    for T in TIMES:
        steps = round((T - tcur) / DT)
        for _ in range(steps):
            Y = solver.step(Y, (T - tcur) / steps)
        tcur = T
        got = {'0': solver.quantities(Y[0]), '2': solver.second(Y)}
        for k, label in (('0', '%s(U)'), ('2', '%s2')):
            for i, X in enumerate(('E', 'Z', 'S')):
                ex, last = series_value(X, int(k), T)
                g = float(got[k][i])
                diff = abs(g - ex)
                digits = -math.log10(diff / abs(ex)) if diff else float('inf')
                worst[(label % X)] = min(worst.get(label % X, 99), digits)
                print(f'    {label % X:<9} {T:5.2f}  {g:+.16e}  {ex:+.16e}  {diff:8.1e}  {digits:5.1f}  '
                      f'{last:8.1e}')
    print(f'    response.py time: {time.time() - t0:.1f} s')
    print('    fewest digits over t = ' + ', '.join(str(t) for t in TIMES) + ': '
          + ', '.join(f'{q} {d:.1f}' for q, d in worst.items()))
    print()
    print(f'total wall time {time.time() - t_start:.0f} s')


if __name__ == '__main__':
    main()
