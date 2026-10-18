"""Evaluate the explicit constants of NOTE.md (finite-time enstrophy-error bound).

Every quantity is computed as an UPPER bound of its definition: time integrals are upper
Riemann sums on a uniform grid where, on each cell, the decreasing factor alpha(t) = |a|e^{-nu t}
is frozen at the left endpoint and every nondecreasing factor at the right endpoint; the
exponent integrals that enter with a negative sign (Phi1 - Psi) use the matching LOWER sums.
A relative slack of 1e-9 is applied to the final constants to cover floating-point rounding
(double precision, not interval arithmetic). Error budget: each cumulative sum has at most
n = 2e4 positive terms (relative rounding <= n * 2^-52 < 5e-12), the exponents are at most 14
(relative error of exp below 1e-11), and each constant is a product/sum of fewer than twenty
such factors, so the accumulated relative rounding is below 1e-10 and the slack covers it.

Agmon constant: C_A^2 = Lambda_4 = sum over nonzero k in Z^3 of |k|^-4. If results/lattice_sums.log
(certified by a separate script) is present its certified bound is used; otherwise a built-in
certified bound is computed here: partial sum over max|k_i| <= R plus the tail bound
  sum_{max|k_i| > R} |k|^-4 <= 4 pi (1/u0 + h/u0^2 + h^2/(3 u0^3)),  h = sqrt(3)/2, u0 = R - 1/2 - h,
which follows from |k| >= |x| - h for x in the unit cube centred at k and from the fact that
those cubes lie in {max|x_i| > R - 1/2} subset {|x| > R - 1/2}.

Usage: python3 -I -B constants.py [--T 0.1 0.25 0.5 1] [--a 1 --c 1 --d 1 --nu 0.0357142857]
       [--n 20000] [--CA value] [--json out.json]
Standard library and NumPy only; a few seconds.
"""
import argparse
import json
import math
import re
from pathlib import Path

import numpy as np

SLACK = 1 + 1e-9


def certified_lambda4(R=60):
    """Certified upper bound of sum_{k != 0} |k|^-4 (partial sum + integral tail)."""
    r = np.arange(-R, R + 1)
    KX, KY, KZ = np.meshgrid(r, r, r, indexing='ij')
    k2 = (KX**2 + KY**2 + KZ**2).astype(float)
    k2[R, R, R] = np.inf
    partial = math.fsum((1.0 / k2**2).ravel().tolist())
    h = math.sqrt(3) / 2
    u0 = R - 0.5 - h
    tail = 4 * math.pi * (1 / u0 + h / u0**2 + h**2 / (3 * u0**3))
    return partial, tail, (partial + tail) * (1 + 1e-12)


def read_certified_CA(path):
    """Read the certified sqrt(Lambda4) from the FINAL TABLE row of results/lattice_sums.log
    (cube partial sum plus closed-form tail bound, rounded up), if the log is present."""
    if not path.exists():
        return None
    m = re.search(r'^\s*Lambda4\s+4\.0\s+[0-9.]+\s+[0-9.]+\s+([0-9.]+)\s+([0-9.]+)', path.read_text(), re.M)
    return float(m.group(2)) if m else None


def chain(a, c, d, nu, CA, T, n, G1_override=None, D1_override=None):
    """Return a dict of the constants of NOTE.md sections 2-5 at the horizon T.

    G1_override / D1_override replace the Lemma 2 bounds G1(t) and D1(t) by given constants
    (used by check_bounds.py for the conditional 'validated propagator' scenario of NOTE.md
    section 7; the result is then NOT a certified bound and is labelled so by the caller).
    """
    dt = T / n
    t = np.linspace(0.0, T, n + 1)
    tl, tr = t[:-1], t[1:]
    g = abs(c) + abs(d)
    assert g >= nu, 'hypothesis (H): |c| + |d| >= nu'
    # base-flow bounds (section 2); hi = upper bound on the cell, lo = lower bound on the cell
    al_hi, al_lo = abs(a) * np.exp(-nu * tl), abs(a) * np.exp(-nu * tr)
    E1 = lambda s: (1 - np.exp(-nu * s)) / nu
    E2 = lambda s: (1 - np.exp(-2 * nu * s)) / (2 * nu)
    g1_hi, g1_lo = abs(d) + abs(a) * g * E1(tr), abs(d) + abs(a) * g * E1(tl)
    g2_hi = abs(d) + abs(a) * g * E1(tr) + 2 * abs(a) * abs(d) * E1(tr) + (2 * a * a * g / nu) * (E1(tr) - E2(tr))
    m1_hi = np.sqrt(al_hi**2 + g**2 + g1_hi**2)
    m1_lo = np.sqrt(al_lo**2 + g**2 + g1_lo**2)
    m2_hi = np.sqrt(al_hi**2 + g**2 + 2 * g1_hi**2 + g2_hi**2)
    mD_hi = np.sqrt(a**2 + (g + g2_hi)**2)      # alpha replaced by |a|: nondecreasing (NOTE.md section 2)
    # exponents at right endpoints (upper sums); L_lo is a lower sum of int (m1 + nu/2)
    Phi1 = np.cumsum((m1_hi - nu) * dt)
    Psi = np.cumsum((2 * m1_hi - nu / 2) * dt)
    Theta = np.cumsum((4 * m1_hi + 1) * dt)
    L_lo = np.concatenate([[0.0], np.cumsum((m1_lo + nu / 2) * dt)[:-1]])   # at left endpoints
    F0 = F1 = 2**-0.5
    # Lemma 2
    G1 = np.exp(Psi) * (F1 + F0 * np.cumsum(m2_hi * np.exp(-L_lo) * dt))
    D1 = (2 / nu) * (0.5 * F1**2 + np.cumsum((2 * m1_hi * G1**2 + m2_hi * F0 * np.exp(Phi1) * G1) * dt))
    if G1_override is not None:
        G1 = np.full_like(G1, float(G1_override))
    if D1_override is not None:
        D1 = np.full_like(D1, float(D1_override))
    beta1 = nu / (2 * CA * G1[-1])
    cs = lambda f: np.cumsum(f * dt)
    # Lemma 3 (q2) and Lemma 4 (mean part); N2 and Nbar have the same expression
    N2 = np.exp(Phi1) * CA * G1 * np.sqrt(tr * D1)
    Q2 = np.sqrt(np.exp(Theta) * (cs(m2_hi**2 * N2**2) + CA**2 * G1**2 * D1 / nu))
    D2 = (2 / nu) * (cs((2 * m1_hi + 0.5) * Q2**2 + 0.5 * m2_hi**2 * N2**2) + CA**2 * G1**2 * D1 / (2 * nu))
    Nbar = N2
    Vbar = np.sqrt(np.exp(Theta) * (cs(m2_hi**2 * Nbar**2) + 2 * CA**2 * G1**2 * D1 / nu))
    Dbar = (4 / nu) * (cs((2 * m1_hi + 0.5) * Vbar**2 + 0.5 * m2_hi**2 * Nbar**2) + CA**2 * G1**2 * D1 / nu)
    # Lemma 5 (r tilde)
    Nr = np.exp(Phi1) * CA * np.sqrt(tr) * (G1 * np.sqrt(D1) + beta1 * (G1 * np.sqrt(Dbar) + Vbar * np.sqrt(D1)))
    Sr = G1**2 * D1 + beta1**2 * (G1**2 * Dbar + Vbar**2 * D1)
    R1 = np.sqrt(np.exp(Theta) * (cs(m2_hi**2 * Nr**2) + 3 * CA**2 * Sr / nu))
    Dr = (2 / nu) * (cs((2 * m1_hi + 0.5) * R1**2 + 0.5 * m2_hi**2 * Nr**2) + 3 * CA**2 * Sr / (2 * nu))
    # Lemma 6 (e2 tilde)
    Ne = np.exp(Phi1) * CA * np.sqrt(tr) * (G1 * np.sqrt(Dbar) + Vbar * np.sqrt(D1) + G1 * np.sqrt(Dr) + R1 * np.sqrt(D1))
    Se = G1**2 * Dbar + Vbar**2 * D1 + G1**2 * Dr + R1**2 * D1
    Et = np.sqrt(np.exp(Theta) * (cs(m2_hi**2 * Ne**2) + 4 * CA**2 * Se / nu))
    De = (2 / nu) * (cs((2 * m1_hi + 0.5) * Et**2 + 0.5 * m2_hi**2 * Ne**2) + 2 * CA**2 * Se / nu)
    # Lemma 7 (e2 bar, L2)
    Ebar = np.exp(Phi1) * CA * np.sqrt(tr) * (Vbar * np.sqrt(Dbar) + Q2 * np.sqrt(D2) + G1 * np.sqrt(De) + Et * np.sqrt(D1)
                                              + beta1 * (Et * np.sqrt(D2) + Q2 * np.sqrt(De)) + beta1**2 * Et * np.sqrt(De))
    # Theorem
    CZ = mD_hi * Ebar + 0.5 * Vbar**2 + 0.5 * Q2**2 + G1 * Et + beta1 * Q2 * Et + 0.5 * beta1**2 * Et**2
    last = lambda x: float(x[-1]) * SLACK
    return {
        'T': T, 'a': a, 'c': c, 'd': d, 'nu': nu, 'C_A': CA, 'grid_cells': n,
        'm1(T)': last(m1_hi), 'm2(T)': last(m2_hi), 'mDelta(T)': last(mD_hi),
        'Phi1': last(Phi1), 'Psi': last(Psi), 'Theta': last(Theta),
        'G1': last(G1), 'D1': last(D1), 'beta1': float(beta1 / SLACK),
        'N2': last(N2), 'Q2': last(Q2), 'D2': last(D2),
        'Vbar': last(Vbar), 'Dbar': last(Dbar), 'Nr': last(Nr), 'R1': last(R1), 'Dr': last(Dr),
        'Ne': last(Ne), 'Etilde': last(Et), 'De': last(De), 'Ebar': last(Ebar), 'C_Z': last(CZ),
        'series': {'t': tr.tolist()[:: max(1, n // 20)], 'G1': G1.tolist()[:: max(1, n // 20)],
                   'Vbar': Vbar.tolist()[:: max(1, n // 20)], 'Etilde': Et.tolist()[:: max(1, n // 20)],
                   'Ebar': Ebar.tolist()[:: max(1, n // 20)], 'C_Z': CZ.tolist()[:: max(1, n // 20)]},
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--T', type=float, nargs='+', default=[0.1, 0.25, 0.5, 1.0])
    p.add_argument('--a', type=float, default=1.0)
    p.add_argument('--c', type=float, default=1.0)
    p.add_argument('--d', type=float, default=1.0)
    p.add_argument('--nu', type=float, default=1 / 28)
    p.add_argument('--n', type=int, default=20000, help='grid cells per horizon (upper sums)')
    p.add_argument('--CA', type=float, default=None, help='override the certified Agmon constant')
    p.add_argument('--json', type=Path, default=None)
    args = p.parse_args()
    here = Path(__file__).resolve().parent
    if args.CA is not None:
        CA, src = args.CA, 'command line'
    else:
        CA = read_certified_CA(here / 'results' / 'lattice_sums.log')
        src = 'results/lattice_sums.log'
        if CA is None:
            partial, tail, lam = certified_lambda4()
            CA, src = math.sqrt(lam), f'built-in: partial {partial:.6f} + tail bound {tail:.6f} (R = 60)'
    print('constants.py: explicit constants of NOTE.md (every number is an upper bound of its definition)')
    print(f'parameters a={args.a} c={args.c} d={args.d} nu={args.nu:.10g}; C_A = {CA:.6f} from {src}; '
          f'Agmon threshold nu/(2 C_A) = {args.nu / (2 * CA):.4e}')
    print(f'ceiling of the all-time condition (PROOF.md, s=4) at these parameters: 7.142e-22 (review/radius_ceiling.log)')
    rows = []
    keys = ['m1(T)', 'm2(T)', 'mDelta(T)', 'Phi1', 'Psi', 'Theta', 'G1', 'D1', 'beta1', 'N2', 'Q2', 'D2',
            'Vbar', 'Dbar', 'Nr', 'R1', 'Dr', 'Ne', 'Etilde', 'De', 'Ebar', 'C_Z']
    for T in args.T:
        r = chain(args.a, args.c, args.d, args.nu, CA, T, args.n)
        rows.append(r)
    print()
    print('quantity        ' + ''.join(f'{"T=" + str(r["T"]):>14s}' for r in rows))
    for k in keys:
        print(f'{k:16s}' + ''.join(f'{r[k]:>14.4e}' for r in rows))
    print()
    print('beta1(T): certified admissible radius for [0,T] (Proposition 1); C_Z(T): |R_Z(t)| <= C_Z(T) b^4 on [0,T] for |b| < beta1(T).')
    if args.json:
        args.json.write_text(json.dumps(rows, indent=1) + '\n')
        print(f'wrote {args.json}')


if __name__ == '__main__':
    main()
