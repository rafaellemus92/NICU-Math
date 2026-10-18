"""Evaluate the explicit constants of NOTE.md (finite-time enstrophy-error bound) in validated
interval arithmetic, and print them with directed rounding: admissible radii rounded DOWN,
error constants rounded UP, so that every printed number is itself a valid bound.

MATHEMATICAL BOUNDS (not errors). Every time integral of NOTE.md sections 2-5 is replaced by an
upper Riemann sum on a uniform grid of n cells: on each cell the decreasing factor
alpha(t) = |a| e^{-nu t} is frozen at the left endpoint and every nondecreasing factor at the
right endpoint; the exponent that enters with a negative sign, Phi1 - Psi = -int (m1 + nu/2),
uses the matching lower sum. The gap between an upper sum and its integral only loosens the
bound; it is a slack, not an error, and no numerical error estimate is needed for it.

NUMERICAL ERROR BUDGET (complete). All arithmetic is interval arithmetic on decimal floating
point numbers with PREC significant digits (module `decimal`, part of the standard library):
  - +, -, *, / : the lower endpoint is computed in a ROUND_FLOOR context and the upper endpoint
    in a ROUND_CEILING context (for products and quotients of intervals of indefinite sign, the
    min/max over the four endpoint products). Subtraction of intervals (the only cancellation
    in the chain, E1 - E2 and 1 - e^{-nu t}) is enclosed, not estimated.
  - sqrt: the context square root is taken at each endpoint, then stepped outward by units in
    the last place until lo*lo <= x and hi*hi >= x hold in EXACT arithmetic (a product of two
    PREC-digit numbers is exact at 2*PREC digits); no rounding property of sqrt is assumed.
  - exp(x): for x >= 0, halve until y = x/2^m <= 1/16, evaluate the Taylor polynomial of degree
    N by Horner's rule with directed rounding (all terms positive, each operation monotone), add
    to the upper endpoint the explicit remainder bound 2 y^(N+1)/(N+1)! (valid for 0 <= y <= 1/16
    since y/(N+2) < 1/2), and square m times with directed rounding; for x < 0 use
    e^x = 1/e^{-x}. Nothing is assumed about the library's exp.
  - nested operations: each intermediate is an interval, so composition is enclosed
    automatically; the final enclosure widths are printed (max relative width over all
    reported quantities, typically below 1e-30), and that line IS the rounding budget.
  - printing: lower bounds (beta1) are the lower endpoint rounded DOWN to SIG significant
    digits (ROUND_FLOOR), upper bounds the upper endpoint rounded UP (ROUND_CEILING); the
    floats returned to check_bounds.py are rounded in the same directions (math.nextafter).
  - input constants: 2^{-1/2} is an enclosure; nu, a, c, d, T are read as exact decimals or
    exact fractions ('1/28' is enclosed, not rounded); the Agmon constant C_A = Lambda4^{1/2}
    is the certified upper bound of results/lattice_sums.log (a 50-digit nearest-rounded sum of
    2.1e5 positive terms, error below 1e-44, plus a closed-form tail bound and a 1e-30 margin,
    printed rounded up), cross-checked here against an independent built-in bound computed with
    an exact integer histogram at R = 60 and directed rounding; the smaller of the two valid
    upper bounds is used.

SUPPORTED PARAMETER RANGE (enforced; the script refuses anything else): nu > 0, T > 0, n >= 1,
a, c, d real with |c| + |d| >= nu certified from the enclosures (hypothesis (H) of NOTE.md,
needed for Phi1 nondecreasing and e^{-Phi1} <= 1), and exponent arguments below 1e4 in
absolute value (sanity bound for the halving count; the chain never approaches it). Inside this
range nothing else is assumed: the monotonicity facts behind the upper sums (alpha decreasing,
E1, E1 - E2, gamma1, gamma2, m_Delta nondecreasing, m1 >= nu) hold for all real a, c, d.

Usage: python3 -I -B constants.py [--T 0.1 0.25 0.5 1] [--a 1 --c 1 --d 1 --nu 1/28]
       [--n 20000] [--CA value] [--json out.json]
Standard library and NumPy (histogram only); pure-Python interval arithmetic, about 20 s per horizon at n = 20000.
"""
import argparse
import json
import math
import re
import sys
from decimal import Decimal, Context, Inexact, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN, localcontext
from pathlib import Path

import numpy as np

PREC = 40            # working digits of every endpoint
SIG = 5              # printed significant digits (directed)
EXP_N = 22           # Taylor degree in exp (remainder 2 (1/16)^23 / 23! < 1e-50)
LO = Context(prec=PREC, rounding=ROUND_FLOOR)
HI = Context(prec=PREC, rounding=ROUND_CEILING)
EXACT = Context(prec=2 * PREC + 2, rounding=ROUND_HALF_EVEN)   # exact for products of two endpoints
D0, D1_, D2_ = Decimal(0), Decimal(1), Decimal(2)
TRAP = Context(prec=1, traps=[Inexact])   # active inside the evaluation: a Decimal operation that bypasses LO/HI/EXACT and is inexact raises
SIXTEENTH = Decimal('0.0625')
PI_HI = Decimal('3.14159265358979323846264338327950288420')    # > pi = 3.14159265358979323846264338327950288419716...


# ----------------------------------------------------------------------------- intervals
def _exp_bounds(x):
    """Decimals (lo, hi) with lo <= e^x <= hi for a Decimal x (see the module docstring)."""
    if x < 0:
        lo, hi = _exp_bounds(x.copy_negate())
        return LO.divide(D1_, hi), HI.divide(D1_, lo)
    if x > 10000:
        raise ValueError('exp argument above the supported range (1e4)')
    m = 0
    y_lo = y_hi = x
    while y_hi > SIXTEENTH:
        y_lo, y_hi, m = LO.divide(y_lo, D2_), HI.divide(y_hi, D2_), m + 1
    s_lo = s_hi = D1_
    for j in range(EXP_N, 0, -1):            # Horner: 1 + y/j * s, all terms positive
        s_lo = LO.add(D1_, LO.multiply(LO.divide(y_lo, j), s_lo))
        s_hi = HI.add(D1_, HI.multiply(HI.divide(y_hi, j), s_hi))
    pw = D1_
    for _ in range(EXP_N + 1):
        pw = HI.multiply(pw, y_hi)
    s_hi = HI.add(s_hi, HI.divide(HI.multiply(D2_, pw), math.factorial(EXP_N + 1)))
    for _ in range(m):
        s_lo, s_hi = LO.multiply(s_lo, s_lo), HI.multiply(s_hi, s_hi)
    return s_lo, s_hi


class Iv:
    """Closed interval [lo, hi] of Decimals; every operation returns an enclosure of the exact result."""
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        self.lo = lo
        self.hi = lo if hi is None else hi
        assert self.lo <= self.hi

    @staticmethod
    def of(x):
        if isinstance(x, Iv):
            return x
        if isinstance(x, str) and '/' in x:
            p, q = x.split('/')
            return Iv.of(p) / Iv.of(q)
        d = Decimal(x)                     # exact for int, float (its binary value) and decimal strings
        if not d.is_finite():
            raise ValueError(f'non-finite parameter {x!r}')
        return Iv(d, d)

    def __repr__(self):
        return f'[{self.lo}, {self.hi}]'

    def __add__(a, b):
        b = Iv.of(b)
        return Iv(LO.add(a.lo, b.lo), HI.add(a.hi, b.hi))
    __radd__ = __add__

    def __sub__(a, b):
        b = Iv.of(b)
        return Iv(LO.subtract(a.lo, b.hi), HI.subtract(a.hi, b.lo))

    def __rsub__(a, b):
        return Iv.of(b) - a

    def __neg__(a):
        return Iv(a.hi.copy_negate(), a.lo.copy_negate())    # copy_negate: exact (unary minus rounds to the default context)

    def __abs__(a):
        if a.lo >= 0:
            return a
        if a.hi <= 0:
            return -a
        return Iv(D0, max(a.lo.copy_abs(), a.hi))

    def __mul__(a, b):
        b = Iv.of(b)
        if a.lo >= 0 and b.lo >= 0:
            return Iv(LO.multiply(a.lo, b.lo), HI.multiply(a.hi, b.hi))
        c = [(x, y) for x in (a.lo, a.hi) for y in (b.lo, b.hi)]
        return Iv(min(LO.multiply(x, y) for x, y in c), max(HI.multiply(x, y) for x, y in c))
    __rmul__ = __mul__

    def __truediv__(a, b):
        b = Iv.of(b)
        if not (b.lo > 0 or b.hi < 0):
            raise ZeroDivisionError('interval divisor contains zero')
        if a.lo >= 0 and b.lo > 0:
            return Iv(LO.divide(a.lo, b.hi), HI.divide(a.hi, b.lo))
        c = [(x, y) for x in (a.lo, a.hi) for y in (b.lo, b.hi)]
        return Iv(min(LO.divide(x, y) for x, y in c), max(HI.divide(x, y) for x, y in c))

    def __rtruediv__(a, b):
        return Iv.of(b) / a

    def sq(a):
        if a.lo >= 0:
            return Iv(LO.multiply(a.lo, a.lo), HI.multiply(a.hi, a.hi))
        if a.hi <= 0:
            return Iv(LO.multiply(a.hi, a.hi), HI.multiply(a.lo, a.lo))
        return Iv(D0, max(HI.multiply(a.lo, a.lo), HI.multiply(a.hi, a.hi)))

    def sqrt(a):
        if a.lo < 0:
            raise ValueError('sqrt of an interval with negative lower endpoint')
        lo, hi = LO.sqrt(a.lo), HI.sqrt(a.hi)
        while EXACT.multiply(lo, lo) > a.lo:      # verified, independent of the rounding of sqrt
            lo = LO.next_minus(lo)
        while EXACT.multiply(hi, hi) < a.hi:
            hi = HI.next_plus(hi)
        return Iv(lo, hi)

    def exp(a):
        return Iv(_exp_bounds(a.lo)[0], _exp_bounds(a.hi)[1])

    def rel_width(a):
        return float(HI.divide(HI.subtract(a.hi, a.lo), a.lo.copy_abs())) if a.lo != 0 else float('inf')


def round_up(d, sig=SIG):
    return Context(prec=sig, rounding=ROUND_CEILING).plus(d)


def round_down(d, sig=SIG):
    return Context(prec=sig, rounding=ROUND_FLOOR).plus(d)


def float_up(d):
    f = float(d)
    return math.nextafter(f, math.inf) if Decimal(f) < d else f


def float_down(d):
    f = float(d)
    return math.nextafter(f, -math.inf) if Decimal(f) > d else f


def fmt(d):
    return f'{d:.{SIG - 1}E}'


# ----------------------------------------------------------------------------- Agmon constant
def certified_lambda4(R=60):
    """Certified upper bound of Lambda_4 = sum_{k != 0} |k|^-4 (Decimals: partial, tail, total).
    Partial sum over the cube max|k_i| <= R from the exact integer histogram of |k|^2 (int64
    bincount), summed with ROUND_CEILING; tail bound T_R <= 4 pi [1/s0 + h/s0^2 + h^2/(3 s0^3)],
    h = sqrt(3)/2, s0 = R + 1/2 - h (the argument is in lattice_sums.py, TAIL BOUND (i)-(iii):
    the unit cubes around the tail points are disjoint, lie in {|x| >= R + 1/2} and carry
    |k| >= |x| - h), evaluated with pi and h rounded up and s0 rounded down, which enlarges it."""
    with localcontext(TRAP):
        return _certified_lambda4(R)


def _certified_lambda4(R):
    ks = np.arange(-R, R + 1, dtype=np.int64)
    n2 = (ks[:, None, None] ** 2 + ks[None, :, None] ** 2 + ks[None, None, :] ** 2).ravel()
    h = np.bincount(n2, minlength=3 * R * R + 1)
    assert h[0] == 1 and int(h.sum()) == (2 * R + 1) ** 3 and h[1:9].tolist() == [6, 12, 8, 6, 24, 24, 0, 12]
    partial = D0
    for n in np.nonzero(h)[0].tolist()[1:]:
        partial = HI.add(partial, HI.divide(Decimal(int(h[n])), Decimal(n * n)))
    hh = (Iv.of(3).sqrt() / 2).hi
    s0 = LO.subtract(LO.add(Decimal(R), Decimal('0.5')), hh)
    tail = (Iv.of(4) * Iv(PI_HI) * (1 / Iv(s0) + Iv(hh) / Iv(s0).sq() + Iv(hh).sq() / (3 * Iv(s0) * Iv(s0).sq()))).hi
    return partial, tail, HI.add(partial, tail)


def read_certified_CA(path):
    """Certified sqrt(Lambda4) (Decimal, an upper bound rounded up to 12 digits) from the FINAL
    TABLE row of results/lattice_sums.log, if present."""
    if not path.exists():
        return None
    m = re.search(r'^\s*Lambda4\s+4\.0\s+[0-9.]+\s+[0-9.]+\s+([0-9.]+)\s+([0-9.]+)', path.read_text(), re.M)
    return Decimal(m.group(2)) if m else None


def agmon_constant(here, override=None):
    """Return (C_A as Iv upper bound, description)."""
    if override is not None:
        ca = Iv.of(override)
        return Iv(ca.hi, ca.hi), 'command line (not certified here)'
    partial, tail, lam_builtin = certified_lambda4()
    with localcontext(TRAP):
        ca_builtin = Iv(lam_builtin).sqrt().hi
    ca_log = read_certified_CA(here / 'results' / 'lattice_sums.log')
    desc = f'built-in R = 60: partial {fmt(round_up(partial, 8))} + tail {fmt(round_up(tail, 8))} -> C_A <= {fmt(round_up(ca_builtin, 8))}'
    if ca_log is not None and ca_log <= ca_builtin:
        return Iv(ca_log), f'results/lattice_sums.log (R = 250): C_A <= {ca_log}; {desc} (consistent)'
    return Iv(ca_builtin), desc + ('' if ca_log is None else f'; log value {ca_log} larger, not used')


# ----------------------------------------------------------------------------- the chain
def check_range(a, c, d, nu, T, n):
    if not (nu.lo > 0):
        raise ValueError('nu must be positive')
    if not (T.lo > 0):
        raise ValueError('T must be positive')
    if not (isinstance(n, int) and n >= 1):
        raise ValueError('n must be a positive integer')
    g = abs(c) + abs(d)
    if not (g.lo >= nu.hi):
        raise ValueError('hypothesis (H) |c| + |d| >= nu is not certified for these parameters; outside the supported range')


def chain(a, c, d, nu, CA, T, n, G1_override=None, D1_override=None, series_every=None):
    """Return a dict of the constants of NOTE.md sections 2-5 at the horizon T.

    Parameters may be Iv, Decimal, int, float or strings ('1/28'). Values in the returned dict:
    floats rounded in the certified direction (beta1 down, everything else up) and, under
    'certified', the directed-rounded decimal strings and the maximal relative enclosure width.
    G1_override / D1_override replace the Lemma 2 bounds G1(t), D1(t) by given constants (the
    what-if scenario of check_bounds.py Table C; the result is then NOT a bound and is labelled
    so by the caller).
    """
    with localcontext(TRAP):
        return _chain(a, c, d, nu, T, CA, n, G1_override, D1_override, series_every)


def _chain(a, c, d, nu, T, CA, n, G1_override, D1_override, series_every):
    a, c, d, nu, T, CA = (Iv.of(x) for x in (a, c, d, nu, T, CA))
    check_range(a, c, d, nu, T, n)
    A, Dd = abs(a), abs(d)
    g = abs(c) + Dd
    dt = T / n
    half = Iv.of('0.5')
    F0 = F1 = 1 / Iv.of(2).sqrt()
    two_a2_g_over_nu = 2 * a.sq() * g / nu
    # exponentials are accumulated multiplicatively (products of enclosures of e^{increment}):
    #   e^{-nu t_{j+1}} = (e^{-nu dt})^{j+1};  e^{Phi1_j} = prod_{i<=j} e^{(m1_hi_i - nu) dt};
    #   Psi = 2 Phi1 + (3 nu/2) t and Theta = 4 Phi1 + (4 nu + 1) t exactly (same cell values);
    #   e^{-L_j} = prod_{i<j} e^{-(m1_lo_i + nu/2) dt}  (lower sum, left endpoint).
    E_nu, E_psi, E_theta = (-nu * dt).exp(), (3 * nu / 2 * dt).exp(), ((4 * nu + 1) * dt).exp()
    one = Iv(D1_)

    def cell(j, el):
        """Cellwise bounds on [t_j, t_{j+1}] from el = e^{-nu t_j}: alpha frozen at the left endpoint,
        nondecreasing factors at the right endpoint (hi), and the lower bound m1_lo used in the
        lower sum. Returns er = e^{-nu t_{j+1}} for the next cell."""
        tr = dt * (j + 1)
        er = el * E_nu
        al_hi, al_lo = A * el, A * er
        e1r, e1l = (1 - er) / nu, (1 - el) / nu
        e2r = (1 - er.sq()) / (2 * nu)
        g1_hi, g1_lo = Dd + A * g * e1r, Dd + A * g * e1l
        g2_hi = Dd + A * g * e1r + 2 * A * Dd * e1r + two_a2_g_over_nu * (e1r - e2r)
        m1_hi = (al_hi.sq() + g.sq() + g1_hi.sq()).sqrt()
        m1_lo = (al_lo.sq() + g.sq() + g1_lo.sq()).sqrt()
        m2_hi = (al_hi.sq() + g.sq() + 2 * g1_hi.sq() + g2_hi.sq()).sqrt()
        mD_hi = (a.sq() + (g + g2_hi).sq()).sqrt()          # alpha replaced by |a|: nondecreasing (NOTE.md section 2)
        return tr, er, m1_hi, m1_lo, m2_hi, mD_hi

    # pass 1: G1(T) and hence beta1 (needed inside Lemmas 5-7)
    el, ePhi, lin_psi, eL, I_G = one, one, one, one, Iv(D0)
    for j in range(n):
        tr, el, m1_hi, m1_lo, m2_hi, mD_hi = cell(j, el)
        ePhi, lin_psi = ePhi * ((m1_hi - nu) * dt).exp(), lin_psi * E_psi
        I_G = I_G + m2_hi * eL * dt
        eL = eL * (-(m1_lo + nu / 2) * dt).exp()
    G1_T = ePhi.sq() * lin_psi * (F1 + F0 * I_G)
    if G1_override is not None:
        G1_T = Iv.of(G1_override)
    beta1 = nu / (2 * CA * G1_T)

    # pass 2: the whole chain, right-endpoint values at every cell
    Phi1 = Psi = Theta = Iv(D0)
    el, ePhi, lin_psi, lin_theta, eL = one, one, one, one, one
    I_G = I_D1 = I_Q2 = I_D2 = I_V = I_Db = I_R1 = I_Dr = I_Et = I_De = Iv(D0)
    half_F1sq = half * F1.sq()
    CA2 = CA.sq()
    series = {k: [] for k in ['t', 'G1', 'Vbar', 'Etilde', 'Ebar', 'C_Z']}
    for j in range(n):
        tr, el, m1_hi, m1_lo, m2_hi, mD_hi = cell(j, el)
        Phi1 = Phi1 + (m1_hi - nu) * dt
        Psi = Psi + (2 * m1_hi - nu / 2) * dt
        Theta = Theta + (4 * m1_hi + 1) * dt
        ePhi, lin_psi, lin_theta = ePhi * ((m1_hi - nu) * dt).exp(), lin_psi * E_psi, lin_theta * E_theta
        I_G = I_G + m2_hi * eL * dt
        eL = eL * (-(m1_lo + nu / 2) * dt).exp()
        ePhi2 = ePhi.sq()
        ePsi, eTheta = ePhi2 * lin_psi, ePhi2.sq() * lin_theta
        # Lemma 2
        G1 = ePsi * (F1 + F0 * I_G)
        I_D1 = I_D1 + (2 * m1_hi * G1.sq() + m2_hi * F0 * ePhi * G1) * dt
        D1 = (2 / nu) * (half_F1sq + I_D1)
        if G1_override is not None:
            G1 = Iv.of(G1_override)
        if D1_override is not None:
            D1 = Iv.of(D1_override)
        G1sq, sqrt_tr, sqrt_D1 = G1.sq(), tr.sqrt(), D1.sqrt()
        m2sq = m2_hi.sq()
        lin = CA2 * G1sq * D1 / nu
        # Lemma 3 (q2) and Lemma 4 (mean part); N2 and Nbar coincide
        N2 = ePhi * CA * G1 * (tr * D1).sqrt()
        N2sq = N2.sq()
        I_Q2 = I_Q2 + m2sq * N2sq * dt
        Q2 = (eTheta * (I_Q2 + lin)).sqrt()
        I_D2 = I_D2 + ((2 * m1_hi + half) * Q2.sq() + half * m2sq * N2sq) * dt
        D2 = (2 / nu) * (I_D2 + lin / 2)
        Nbar, Nbarsq = N2, N2sq
        I_V = I_V + m2sq * Nbarsq * dt
        Vbar = (eTheta * (I_V + 2 * lin)).sqrt()
        I_Db = I_Db + ((2 * m1_hi + half) * Vbar.sq() + half * m2sq * Nbarsq) * dt
        Dbar = (4 / nu) * (I_Db + lin)
        sqrt_Dbar = Dbar.sqrt()
        # Lemma 5 (r tilde)
        Nr = ePhi * CA * sqrt_tr * (G1 * sqrt_D1 + beta1 * (G1 * sqrt_Dbar + Vbar * sqrt_D1))
        Sr = G1sq * D1 + beta1.sq() * (G1sq * Dbar + Vbar.sq() * D1)
        I_R1 = I_R1 + m2sq * Nr.sq() * dt
        R1 = (eTheta * (I_R1 + 3 * CA2 * Sr / nu)).sqrt()
        I_Dr = I_Dr + ((2 * m1_hi + half) * R1.sq() + half * m2sq * Nr.sq()) * dt
        Dr = (2 / nu) * (I_Dr + 3 * CA2 * Sr / (2 * nu))
        # Lemma 6 (e2 tilde)
        Ne = ePhi * CA * sqrt_tr * (G1 * sqrt_Dbar + Vbar * sqrt_D1 + G1 * Dr.sqrt() + R1 * sqrt_D1)
        Se = G1sq * Dbar + Vbar.sq() * D1 + G1sq * Dr + R1.sq() * D1
        I_Et = I_Et + m2sq * Ne.sq() * dt
        Et = (eTheta * (I_Et + 4 * CA2 * Se / nu)).sqrt()
        I_De = I_De + ((2 * m1_hi + half) * Et.sq() + half * m2sq * Ne.sq()) * dt
        De = (2 / nu) * (I_De + 2 * CA2 * Se / nu)
        sqrt_De = De.sqrt()
        # Lemma 7 (e2 bar, L2)
        Ebar = ePhi * CA * sqrt_tr * (Vbar * sqrt_Dbar + Q2 * D2.sqrt() + G1 * sqrt_De + Et * sqrt_D1
                                      + beta1 * (Et * D2.sqrt() + Q2 * sqrt_De) + beta1.sq() * Et * sqrt_De)
        # Theorem
        CZ = mD_hi * Ebar + half * Vbar.sq() + half * Q2.sq() + G1 * Et + beta1 * Q2 * Et + half * beta1.sq() * Et.sq()
        if series_every and (j + 1) % series_every == 0:
            for k, v in (('t', tr), ('G1', G1), ('Vbar', Vbar), ('Etilde', Et), ('Ebar', Ebar), ('C_Z', CZ)):
                series[k].append(float_up(v.hi))
    upper = {'m1(T)': m1_hi, 'm2(T)': m2_hi, 'mDelta(T)': mD_hi, 'Phi1': Phi1, 'Psi': Psi, 'Theta': Theta,
             'G1': G1, 'D1': D1, 'N2': N2, 'Q2': Q2, 'D2': D2, 'Vbar': Vbar, 'Dbar': Dbar, 'Nr': Nr, 'R1': R1,
             'Dr': Dr, 'Ne': Ne, 'Etilde': Et, 'De': De, 'Ebar': Ebar, 'C_Z': CZ}
    out = {'T': float(T.hi), 'a': float(a.hi), 'c': float(c.hi), 'd': float(d.hi), 'nu': float(nu.hi),
           'C_A': float_up(CA.hi), 'grid_cells': n, 'beta1': float_down(beta1.lo)}
    cert = {'beta1': str(round_down(beta1.lo)), 'C_A': str(CA.hi)}
    width = beta1.rel_width()
    for k, v in upper.items():
        out[k] = float_up(v.hi)
        cert[k] = str(round_up(v.hi))
        width = max(width, v.rel_width())
    out['certified'] = cert
    out['max_relative_enclosure_width'] = width
    out['series'] = series
    return out


KEYS = ['m1(T)', 'm2(T)', 'mDelta(T)', 'Phi1', 'Psi', 'Theta', 'G1', 'D1', 'beta1', 'N2', 'Q2', 'D2',
        'Vbar', 'Dbar', 'Nr', 'R1', 'Dr', 'Ne', 'Etilde', 'De', 'Ebar', 'C_Z']


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--T', nargs='+', default=['0.1', '0.25', '0.5', '1'], help='horizons (exact decimals or p/q)')
    p.add_argument('--a', default='1')
    p.add_argument('--c', default='1')
    p.add_argument('--d', default='1')
    p.add_argument('--nu', default='1/28')
    p.add_argument('--n', type=int, default=20000, help='grid cells per horizon (upper sums)')
    p.add_argument('--CA', default=None, help='override the certified Agmon constant (then not certified)')
    p.add_argument('--json', type=Path, default=None)
    args = p.parse_args()
    here = Path(__file__).resolve().parent
    CA, src = agmon_constant(here, args.CA)
    nu = Iv.of(args.nu)
    print('constants.py: explicit constants of NOTE.md in validated interval arithmetic '
          f'({PREC} decimal digits, directed rounding; printed to {SIG} significant digits: beta1 rounded DOWN, all others UP)')
    print(f'parameters a={args.a} c={args.c} d={args.d} nu={args.nu}; supported range enforced: nu > 0, T > 0, |c|+|d| >= nu')
    print(f'C_A: {src}; Agmon threshold nu/(2 C_A) >= {fmt(round_down((nu / (2 * CA)).lo))}')
    print('ceiling of the all-time condition (PROOF.md, s = 4) at these parameters: 7.2e-22 rounded up from the double-precision '
          '7.142e-22 of review/radius_ceiling.log (a ceiling on a sufficient condition, not an admissible radius)')
    rows = []
    for T in args.T:
        rows.append(chain(args.a, args.c, args.d, args.nu, CA, T, args.n, series_every=max(1, args.n // 20)))
    print()
    print('quantity        ' + ''.join(f'{"T=" + str(r["T"]):>14s}' for r in rows))
    for k in KEYS:
        print(f'{k:16s}' + ''.join(f'{fmt(Decimal(r["certified"][k])):>14s}' for r in rows))
    print()
    print(f'rounding budget: maximal relative width of the enclosures over all reported quantities '
          f'{max(r["max_relative_enclosure_width"] for r in rows):.1e} (the upper-sum slack is not an error; see the docstring)')
    print('beta1(T): certified admissible radius for [0,T] (Proposition 1; strict inequality |b| < beta1(T)); '
          'C_Z(T): |R_Z(t)| <= C_Z(T) b^4 on [0,T] for |b| < beta1(T).')
    if args.json:
        args.json.write_text(json.dumps(rows, indent=1) + '\n')
        print(f'wrote {args.json}')


if __name__ == '__main__':
    main()
