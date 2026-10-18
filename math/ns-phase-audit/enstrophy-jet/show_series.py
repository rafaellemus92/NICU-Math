#!/usr/bin/env python3
"""Print the exact enstrophy series in readable form (reads results/series.json; no flint needed).

  python3 show_series.py              t^6, t^7, t^8 polynomials (default)
  python3 show_series.py --orders 9   any orders
  python3 show_series.py --rules      check the selection rules on every c[n,m], n <= 14
  python3 show_series.py --reach      partial sums of the phase amplitudes at nu = 1/28
  python3 show_series.py --all        everything (this is what results/series_summary.txt holds)

Conventions: Z(t,phi) = sum_n sum_m c[n,m](nu) t^n e^{i m phi}  (Laurent coefficients).
Because c[n,-m] = c[n,m], the cosine form is  [t^n]Z = c[n,0] + sum_{m>=1} 2 c[n,m] cos(m phi).
"""
import argparse
import json
import os
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'results', 'series.json')))
NMAX = max(int(n) for n in S['orders'])


def poly(n, m):
    """c[n,m] as a list of Fractions (index = power of nu); [] if absent."""
    return [Fr(a) for a in S['orders'].get(str(n), {}).get(str(m), [])]


def ev(p, nu):
    return sum(a * nu ** d for d, a in enumerate(p))


def fmt(p, scale=1):
    terms = []
    for d, a in enumerate(p):
        a = a * scale
        if a == 0:
            continue
        sgn = '-' if a < 0 else '+'
        mag = abs(a)
        num = str(mag) if mag.denominator == 1 else f'({mag})'
        nu = '' if d == 0 else (' nu' if d == 1 else f' nu^{d}')
        if d > 0 and mag == 1:
            num, nu = '', nu.strip()
        terms.append(f'{sgn} {num}{nu}')
    if not terms:
        return '0'
    s = ' '.join(terms)
    return s[2:] if s.startswith('+ ') else '-' + s[2:]


def harmonics(n):
    return sorted(int(m) for m in S['orders'].get(str(n), {}) if int(m) >= 0)


def show_orders(orders):
    nu28 = Fr(1, 28)
    for n in orders:
        print(f'\n=== [t^{n}] Z ===')
        hs = harmonics(n)
        absent = [m for m in range(0, 5) if m not in hs]
        for m in hs:
            p = poly(n, m)
            print(f'  Laurent c[{n},{m}] = {fmt(p)}')
            if m == 0:
                print(f'     constant term        = c[{n},0];  at nu=0: {float(ev(p, 0)):+.10g};  at nu=1/28: {float(ev(p, nu28)):+.10g}')
            else:
                print(f'     cos({m} phi) coefficient = 2c[{n},{m}] = {fmt(p, 2)}')
                print(f'                            at nu=0: {float(2*ev(p, 0)):+.10g};  at nu=1/28: {float(2*ev(p, nu28)):+.10g}')
        print(f'  no harmonic m in {absent} at this order')
        cs = ' '.join(f'{float((1 if m == 0 else 2) * ev(poly(n, m), nu28)):+.10f}' + ('' if m == 0 else f' cos({m}phi)')
                      for m in hs)
        print(f'  at nu=1/28: [t^{n}]Z = {cs}')


def bmin(M):
    return 0 if M == 0 else (1 if M == 1 else 3 * M)


def show_rules():
    print('\n=== Selection rules on every c[n,m], n <= %d ===' % NMAX)
    print('  rule A (time-reversal parity): only powers nu^p with p = n+m (mod 2) occur')
    print('  rule B (3m nonlinear steps):  deg c[n,m] <= n - b(m), b(0)=0, b(1)=1, b(m)=3m for m>=2')
    print('  "allowed" = powers permitted by A and B together; "present" = nonzero powers in series.json')
    allA = allB = full = sym = True
    for n in range(NMAX + 1):
        row = []
        for M in range(0, n // 3 + 2):
            p = poly(n, M)
            present = [d for d, a in enumerate(p) if a != 0]
            allowed = [d for d in range(0, n - bmin(M) + 1) if (d - n - M) % 2 == 0] if n >= bmin(M) else []
            allA &= all((d - n - M) % 2 == 0 for d in present)
            allB &= all(d <= n - bmin(M) for d in present)
            full &= present == allowed
            sym &= poly(n, -M) == p
            if present or allowed:
                row.append(f'm={M}: {present}' + ('' if present == allowed else f' (allowed {allowed})'))
        print(f'  n={n:2d}  ' + '; '.join(row))
    print(f'  rule A holds for every c[n,m]: {allA}')
    print(f'  rule B holds for every c[n,m]: {allB}')
    print(f'  every allowed power is actually present (rules are sharp here): {full}')
    print(f'  c[n,-m] = c[n,m] for all n, m: {sym}')
    ok = True
    for n in range(NMAX):
        for m in set(S['energy_orders'].get(str(n + 1), {})) | set(S['orders'].get(str(n), {})):
            e = [Fr(a) for a in S['energy_orders'].get(str(n + 1), {}).get(m, [])]
            z = [Fr(a) for a in S['orders'].get(str(n), {}).get(m, [])]
            lhs = [(n + 1) * a for a in e]
            rhs = [Fr(0)] + [-2 * a for a in z]
            L = max(len(lhs), len(rhs))
            lhs += [Fr(0)] * (L - len(lhs)); rhs += [Fr(0)] * (L - len(rhs))
            while lhs and lhs[-1] == 0 and rhs[-1] == 0:
                lhs.pop(); rhs.pop()
            ok &= lhs == rhs
    print(f'  energy identity (n+1)[t^(n+1)]E = -2 nu [t^n]Z, n < {NMAX}, every harmonic: {ok}')
    first = {}
    for M in range(1, 6):
        ns = [n for n in range(NMAX + 1) if any(a != 0 for a in poly(n, M))]
        first[M] = ns[0] if ns else None
    print('  first order at which harmonic m appears: ' + ', '.join(f'm={M}: t^{first[M]}' for M in first if first[M] is not None)
          + ('' if first[5] is None else '') + f'  (m=5 would first appear at t^15, beyond n={NMAX})')
    for M in (2, 3, 4):
        print(f'  cos({M} phi) at its first order t^{3*M}: 2c[{3*M},{M}] = {fmt(poly(3*M, M), 2)} = {float(2*poly(3*M, M)[0]):+.6e}'
              f';  next order 2c[{3*M+1},{M}] = {fmt(poly(3*M+1, M), 2)}')


def show_reach(nu=Fr(1, 28)):
    print(f'\n=== How far the truncated jet reaches (nu = {nu}) ===')
    print('  B(t)   = cos(phi) amplitude  = sum_n 2c[n,1] t^n')
    print('  A2(t)  = cos(2phi) amplitude = sum_n 2c[n,2] t^n')
    print('  curv(t)= d2Z/dphi2 at phi=0  = -sum_n sum_m m^2 2c[n,m] t^n')
    print('  S_K = partial sum through t^K. With only C + B cos phi + A2 cos 2phi, an interior')
    print('  maximum in phi needs |B| < 4|A2|.')
    c = {n: {m: float(ev(poly(n, m), nu)) for m in range(0, 5)} for n in range(NMAX + 1)}
    for t in (0.5, 1.0, 1.5, 2.0, 4.0):
        print(f'\n  t = {t}')
        print('     K        B(t)          A2(t)         curv(t)     4|A2|/|B|')
        for K in range(6, NMAX + 1):
            B = sum(2 * c[n][1] * t ** n for n in range(K + 1))
            A2 = sum(2 * c[n][2] * t ** n for n in range(K + 1))
            cv = -sum(m * m * 2 * c[n][m] * t ** n for n in range(K + 1) for m in range(1, 5))
            print(f'    {K:2d}  {B:+13.6e}  {A2:+13.6e}  {cv:+13.6e}  {abs(4*A2/B):10.3g}')


def main():
    ap = argparse.ArgumentParser(description='Readable view of results/series.json')
    ap.add_argument('--orders', type=int, nargs='*')
    ap.add_argument('--rules', action='store_true')
    ap.add_argument('--reach', action='store_true')
    ap.add_argument('--all', action='store_true')
    a = ap.parse_args()
    print(f'results/series.json: orders 0..{NMAX}, complete={S["complete"]}; {S["convention"]}')
    if a.all or a.orders or not (a.rules or a.reach):
        show_orders(a.orders or [6, 7, 8])
    if a.all or a.rules:
        show_rules()
    if a.all or a.reach:
        show_reach()


if __name__ == '__main__':
    main()
