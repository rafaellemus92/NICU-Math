#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
lattice_sums.py -- rigorously certified upper bounds (and two-sided enclosures) for the
lattice sums that enter Agmon/Sobolev constants on the 2*pi-periodic torus T^3.

Run:  python -I lattice_sums.py        (numpy only; no other third-party imports)

DEFINITIONS  (k in Z^3 \ {0}, |k| Euclidean)
  Lambda4      = sum_k |k|^-4
  Lambda4_osc  = sum_{k_z != 0} |k|^-4
  Lambda4_mean = sum_{k_z = 0, (k_x,k_y) != 0} |k|^-4          (2-D lattice sum over Z^2 \ {0})
  Lambda3      = sum_k |k|^-3.5
Derived constants: C = sqrt(Lambda).  E.g. for mean-zero f with volume-normalised Fourier
coefficients, Cauchy-Schwarz gives ||f||_inf <= sum_k |f_k| <= Lambda4^{1/2} ||Delta f||_{L^2},
and ||f||_inf <= Lambda3^{1/2} ||f||_{H^{7/4}} (homogeneous norm, |k|^{7/2} weights).

METHOD
  Every sum is split as  S = P_R + T_R  with
    P_R = sum over the cube  max_i |k_i| <= R,   T_R = sum over max_i |k_i| >= R+1.
  P_R is computed from the exact integer histogram  r(n) = #{k in cube : |k|^2 = n}
  (numpy.bincount on int64 -- exact), so each distinct value n = |k|^2 contributes r(n) * n^(-p/2)
  once.  The float64 value is  math.fsum  of these (positive) terms; the same sum is recomputed
  in 50-digit decimal arithmetic to measure the realised float64 rounding and to feed the
  certified bound (so float rounding plays no role in the certification).

TAIL BOUND (cube, upper) -- the formula actually used for the "certified upper bound" column
  Let p > 3, L = R + 1/2, a = sqrt(3)/2, E = {k in Z^3 : max_i |k_i| >= R+1}, Q_k = k + [-1/2,1/2]^3.
  (i)   The cubes Q_k (k in E) have pairwise disjoint interiors and unit volume, hence
            T_R = sum_{k in E} |k|^-p = sum_{k in E} int_{Q_k} |k|^-p dx.
  (ii)  For x in Q_k: |x - k| <= a (half body diagonal), so |k| >= |x| - a.  Moreover for k in E
        and x in Q_k,  max_i |x_i| >= max_i |k_i| - 1/2 >= R + 1/2 = L, so |x| >= L > a (needs R >= 1).
        Hence |x| - a > 0 and, since t -> t^-p is decreasing on (0,inf),
            |k|^-p <= (|x| - a)^-p        pointwise on Q_k.
  (iii) Union_{k in E} Q_k  is contained in  Omega = {x : max_i |x_i| >= L}   (shown in (ii)),
        and Omega is contained in B = {x : |x| >= L}  because |x| >= max_i |x_i|.
        The integrand (|x|-a)^-p is positive on B (|x| >= L > a), so enlarging the domain of
        integration from Omega to B can only increase the integral.
  Therefore
        T_R <= int_Omega (|x|-a)^-p dx <= int_B (|x|-a)^-p dx = 4 pi int_L^inf (r-a)^-p r^2 dr
            = 4 pi int_{s0}^inf s^-p (s+a)^2 ds,          s0 = L - a = R + 1/2 - sqrt(3)/2,
            = 4 pi [ s0^(3-p)/(p-3) + 2 a s0^(2-p)/(p-2) + a^2 s0^(1-p)/(p-1) ].          (T3)
  For p = 4:    T_R <= 4 pi [ 1/s0 + a/s0^2 + a^2/(3 s0^3) ].
  For p = 3.5:  T_R <= 4 pi [ 2 s0^-1/2 + (4a/3) s0^-3/2 + (2a^2/5) s0^-5/2 ].
  2-D (Lambda4_mean): identical argument with unit squares, a2 = sqrt(2)/2,
        Omega2 = {max(|x1|,|x2|) >= L} subset {|x| >= L}, polar measure 2 pi r dr:
        T_R <= 2 pi int_{s0}^inf s^-p (s + a2) ds = 2 pi [ s0^(2-p)/(p-2) + a2 s0^(1-p)/(p-1) ],
        s0 = R + 1/2 - sqrt(2)/2.                                                            (T2)
  Lambda4_osc: its tail is the sub-sum (k_z != 0) of the positive Lambda4 tail, so (T3) applies.

TAIL ENCLOSURE (ball partial sums, two-sided) -- independent cross-check and sharper certification
  Ball partial sum P'_R = sum_{0<|k|<=R}, tail T'_R = sum_{|k|>R}, R > 2a.
    upper: for |k| > R and x in Q_k, |x| >= |k| - a > R - a, so Q_k subset {|x| > R-a};
           there |k| >= |x| - a > R - 2a > 0 gives |k|^-p <= (|x|-a)^-p; hence
               T'_R <= 4 pi int_{|x|>R-a} (|x|-a)^-p dx = 4 pi int_{R-2a}^inf s^-p (s+a)^2 ds.
    lower: the cubes Q_k tile R^3 (boundaries have measure 0); every x with |x| > R+a lies in a Q_k
           with |k| >= |x| - a > R, so {|x| > R+a} subset Union_{|k|>R} Q_k (a.e.), and on Q_k
           |k| <= |x| + a gives |k|^-p >= (|x|+a)^-p; hence
               T'_R >= 4 pi int_{|x|>R+a} (|x|+a)^-p dx = 4 pi int_{R+2a}^inf s^-p (s-a)^2 ds.
  (2-D analogues with 2 pi, a2 and (s +- a2).)  Lambda4_osc = Lambda4 - Lambda4_mean term by term,
  so its tail lies in [lo3 - hi2, hi3 - lo2].  The enclosure width is ~ 16 pi a R^(2-p).

ROUNDING / CERTIFICATION
  All closed-form bounds are evaluated in 50-digit decimal arithmetic (sqrt is correctly rounded
  there), a margin of 1e-30 is added, and the printed certified numbers are produced with directed
  rounding (upper bounds rounded UP to 12 significant digits, lower bounds rounded DOWN), so every
  printed certified number is itself a valid bound.  sqrt(certified upper) is a valid upper bound
  for sqrt(Lambda) by monotonicity.  The float64 partial sums (math.fsum of positive terms, each
  term computed with <= ~1.5 ulp error) carry an a-priori relative error <= 5e-16; the realised
  error against the 50-digit value is printed.

ESTIMATES (NOT certified, reference only)
  (E1) cube:  P_R + C_p L^(3-p),   C_p = int_{max|y_i|>=1} |y|^-p dy
                                      = 6/(p-3) * int_{[-1,1]^2} (1+x^2+y^2)^(-p/2) dx dy
       (midpoint-rule approximation of the tail; C_p by Gauss-Legendre; the 2-D constant is
        4/(p-2) * int_{-1}^{1} (1+y^2)^(-p/2) dy, which equals 1 + pi/2 for p = 4).
  (E2) ball "4 pi / R"-type:  P'_R + 4 pi R^(3-p)/(p-3)      (2-D: P'_R + 2 pi R^(2-p)/(p-2)).
  (E3) midpoint of the certified ball enclosure.
"""
import math
import sys
import time
from decimal import Decimal, getcontext, Context, ROUND_CEILING, ROUND_FLOOR

import numpy as np

getcontext().prec = 50
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459")
A3 = Decimal(3).sqrt() / 2          # a  = sqrt(3)/2  : half body-diagonal of the unit cube
A2 = Decimal(2).sqrt() / 2          # a2 = sqrt(2)/2  : half diagonal of the unit square
HALF = Decimal(1) / 2
MARGIN = Decimal("1e-30")

QUANTITIES = [  # name, p, kind
    ("Lambda4",      4.0, "3d"),
    ("Lambda4_osc",  4.0, "osc"),
    ("Lambda4_mean", 4.0, "2d"),
    ("Lambda3",      3.5, "3d"),
]
R_LIST = [50, 100, 150, 200, 250]
TARGET = 0.005          # certified tail bound <= 0.5 % of the partial sum
SIG = 12                # significant digits of printed certified numbers


# ----------------------------------------------------------------------------- decimal helpers
def dround(d, mode, sig=SIG):
    """Round Decimal d to `sig` significant digits with directed rounding (returns Decimal)."""
    return Context(prec=sig, rounding=mode).plus(d)


def up(d, sig=SIG):
    return str(dround(d, ROUND_CEILING, sig))


def dn(d, sig=SIG):
    return str(dround(d, ROUND_FLOOR, sig))


def dpow(x, q):
    """x**q for Decimal x > 0 and half-integer q, via integer powers and one correctly rounded sqrt."""
    q = Decimal(q)
    m2 = 2 * q
    assert m2 == m2.to_integral_value(), "exponent must be a half-integer"
    m = int(m2)
    if m % 2 == 0:
        return x ** (m // 2)
    k = (m - 1) // 2                      # q = k + 1/2
    return x ** k * x.sqrt()


def I3(s0, a, p, sign):
    """4 pi * int_{s0}^inf s^-p (s + sign*a)^2 ds   (closed form, p > 3, s0 > 0)."""
    p = Decimal(p)
    return 4 * PI * (dpow(s0, 3 - p) / (p - 3)
                     + sign * 2 * a * dpow(s0, 2 - p) / (p - 2)
                     + a * a * dpow(s0, 1 - p) / (p - 1))


def I2(s0, a, p, sign):
    """2 pi * int_{s0}^inf s^-p (s + sign*a) ds   (closed form, p > 2, s0 > 0)."""
    p = Decimal(p)
    return 2 * PI * (dpow(s0, 2 - p) / (p - 2) + sign * a * dpow(s0, 1 - p) / (p - 1))


def check_antiderivatives():
    """Numerically verify the closed forms I3, I2 (composite Simpson on [s0, S] vs I(s0)-I(S))."""
    worst = 0.0
    for p in (4.0, 3.5):
        for sign in (+1, -1):
            for (fun, a, dim) in ((I3, float(A3), 3), (I2, float(A2), 2)):
                s0, S, N = 7.0, 70.0, 200_000
                s = np.linspace(s0, S, 2 * N + 1)
                f = s ** (-p) * (s + sign * a) ** (dim - 1)
                w = np.ones_like(s); w[1:-1:2] = 4; w[2:-1:2] = 2
                num = (2 * math.pi if dim == 2 else 4 * math.pi) * (S - s0) / (6 * N) * float(np.dot(w, f))
                cf = float(fun(Decimal(s0), Decimal(a), p, sign) - fun(Decimal(S), Decimal(a), p, sign))
                rel = abs(num - cf) / abs(cf)
                worst = max(worst, rel)
    print(f"[check] closed-form tail antiderivatives vs Simpson quadrature: worst rel. diff = {worst:.2e}")
    assert worst < 1e-9


# ----------------------------------------------------------------------------- lattice histograms
def hist(R):
    """Exact integer histograms over the cube max|k_i| <= R.
    h3[n] = #{k in Z^3, max|k_i|<=R : |k|^2 = n};  h2[n] = same restricted to k_z = 0 (= Z^2 counts)."""
    ks = np.arange(-R, R + 1, dtype=np.int64)
    n2d = (ks[:, None] ** 2 + ks[None, :] ** 2).ravel()
    L = 3 * R * R + 1
    h2 = np.bincount(n2d, minlength=L)
    h3 = h2.copy()
    for kz in range(1, R + 1):
        h3 += 2 * np.bincount(n2d + kz * kz, minlength=L)
    assert h3.sum() == (2 * R + 1) ** 3 and h2.sum() == (2 * R + 1) ** 2
    assert h3[0] == 1 and h2[0] == 1
    # r_3(n) for small n: 6, 12, 8, 6, 24, 24, 0, 12 ; r_2(n): 4, 4, 0, 4, 8, 0, 0, 4
    assert h3[1:9].tolist() == [6, 12, 8, 6, 24, 24, 0, 12]
    assert h2[1:9].tolist() == [4, 4, 0, 4, 8, 0, 0, 4]
    return h2, h3


def sum_float(h, p, nmax):
    """float64: math.fsum of r(n) * n^(-p/2), n = 1..nmax (terms are positive)."""
    c = h[1:nmax + 1]
    idx = np.nonzero(c)[0]
    n = (idx + 1).astype(np.float64)
    cc = c[idx].astype(np.float64)
    if p == 4.0:
        t = cc / (n * n)                  # n*n exact (< 2^53); one correctly rounded division
    else:
        t = cc * np.power(n, -p / 2)      # pow <= 1 ulp, product 0.5 ulp
    return math.fsum(t.tolist())


def sum_dec(h, p, nmax):
    """50-digit decimal: same sum, n^(-1.75) = 1/(n*sqrt(n*sqrt(n))) using correctly rounded sqrt."""
    c = h[1:nmax + 1]
    idx = np.nonzero(c)[0]
    tot = Decimal(0)
    if p == 4.0:
        for i, cnt in zip(idx.tolist(), c[idx].tolist()):
            n = Decimal(i + 1)
            tot += cnt / (n * n)
    elif p == 3.5:
        for i, cnt in zip(idx.tolist(), c[idx].tolist()):
            n = Decimal(i + 1)
            tot += cnt / (n * (n * n.sqrt()).sqrt())
    else:
        raise ValueError(p)
    return tot


# ----------------------------------------------------------------------------- bounds
def tail_cube_upper(kind, p, R):
    R = Decimal(R)
    if kind in ("3d", "osc"):
        return I3(R + HALF - A3, A3, p, +1)
    return I2(R + HALF - A2, A2, p, +1)


def tail_ball_enclosure(kind, p, R):
    R = Decimal(R)
    lo3, hi3 = I3(R + 2 * A3, A3, p, -1), I3(R - 2 * A3, A3, p, +1)
    lo2, hi2 = I2(R + 2 * A2, A2, p, -1), I2(R - 2 * A2, A2, p, +1)
    if kind == "3d":
        return lo3, hi3
    if kind == "2d":
        return lo2, hi2
    return max(Decimal(0), lo3 - hi2), hi3 - lo2


def select(kind, h2, h3, R, ball):
    """Histogram and nmax for a quantity; ball=True restricts to |k|^2 <= R^2."""
    if kind == "3d":
        h, nmax = h3, 3 * R * R
    elif kind == "2d":
        h, nmax = h2, 2 * R * R
    else:
        h, nmax = h3 - h2, 3 * R * R
    if ball:
        nmax = R * R
    return h, nmax


def gauss_constants(p):
    """Non-certified: C_p (3-D) and C2_p (2-D) cube-complement integrals by Gauss-Legendre."""
    xg, wg = np.polynomial.legendre.leggauss(80)
    X, Y = np.meshgrid(xg, xg)
    W = np.outer(wg, wg)
    C3 = 6.0 / (p - 3.0) * float(np.sum(W * (1.0 + X ** 2 + Y ** 2) ** (-p / 2)))
    C2 = 4.0 / (p - 2.0) * float(np.sum(wg * (1.0 + xg ** 2) ** (-p / 2)))
    return C3, C2


# ----------------------------------------------------------------------------- main
def main():
    t_start = time.time()
    print("lattice_sums.py -- certified lattice-sum bounds on T^3")
    print(f"python {sys.version.split()[0]}  numpy {np.__version__}  decimal precision {getcontext().prec}")
    print(f"a = sqrt(3)/2 = {A3}\na2 = sqrt(2)/2 = {A2}")
    check_antiderivatives()
    C3_4, C2_4 = gauss_constants(4.0)
    C3_35, C2_35 = gauss_constants(3.5)
    print(f"[check] 2-D cube-complement constant C2_4 = {C2_4:.15f}, closed form 1+pi/2 = {1 + math.pi / 2:.15f}")
    assert abs(C2_4 - (1 + math.pi / 2)) < 1e-12
    print()

    cube = {}       # (name, R) -> dict
    hists = {}
    for R in R_LIST:
        t1 = time.time()
        h2, h3 = hist(R)
        th = time.time() - t1
        hists[R] = (h2, h3)
        for name, p, kind in QUANTITIES:
            h, nmax = select(kind, h2, h3, R, ball=False)
            t2 = time.time()
            Pf = sum_float(h, p, nmax)
            tf = time.time() - t2
            t2 = time.time()
            Pd = sum_dec(h, p, nmax)
            td = time.time() - t2
            T = tail_cube_upper(kind, p, R)
            U = Pd + T + MARGIN
            cube[(name, R)] = dict(p=p, kind=kind, Pf=Pf, Pd=Pd, T=T, U=U,
                                   n_points=(2 * R + 1) ** 3 if kind != "2d" else (2 * R + 1) ** 2,
                                   t_hist=th, t_f=tf, t_d=td)

    # ---------------- convergence tables (cube) ----------------
    print("=" * 118)
    print("CUBE PARTIAL SUMS  P_R = sum over max|k_i| <= R,  certified upper bound U_R = P_R + (T3)/(T2) tail bound")
    print("(printed certified numbers are rounded UP to 12 significant digits; realised float64 rounding = |fsum - 50-digit|)")
    print("=" * 118)
    chosen = {}
    for name, p, kind in QUANTITIES:
        print(f"\n{name}  (p = {p}, kind = {kind})")
        print(f"{'R':>4} {'lattice pts':>12} {'partial (fsum, float64)':>24} {'float rounding':>14} "
              f"{'tail bound':>14} {'certified upper':>16} {'tail/partial':>12} {'time[s]':>8}")
        for R in R_LIST:
            d = cube[(name, R)]
            err = abs(Decimal(d["Pf"]) - d["Pd"])
            ratio = float(d["T"] / d["Pd"])
            flag = ""
            if ratio <= TARGET and name not in chosen:
                chosen[name] = R
                flag = "  <- first R meeting 0.5 %"
            print(f"{R:>4} {d['n_points']:>12d} {d['Pf']:>24.16g} {float(err):>14.2e} "
                  f"{up(d['T'], 8):>14} {up(d['U']):>16} {100 * ratio:>11.3f}% {d['t_hist'] + d['t_f'] + d['t_d']:>8.2f}{flag}")
        # predicted minimal R from the bound formula (partial at R_LIST[0] is a lower bound for all P_R)
        P0 = cube[(name, R_LIST[0])]["Pd"]
        Rmin = None
        for Rt in range(2, 200_001):
            if tail_cube_upper(kind, p, Rt) <= Decimal(TARGET) * P0:
                Rmin = Rt
                break
        if Rmin is None:
            print(f"     minimal R for the 0.5 % criterion: > 200000 (infeasible)")
        else:
            print(f"     minimal R for the 0.5 % criterion (from the tail formula): R = {Rmin}"
                  f"  -> {(2 * Rmin + 1) ** (2 if kind == '2d' else 3):.3e} lattice points")

    # ---------------- ball enclosures from the largest histogram ----------------
    Rmax = R_LIST[-1]
    h2, h3 = hists[Rmax]
    print()
    print("=" * 118)
    print("BALL PARTIAL SUMS  P'_R = sum over 0 < |k| <= R  with TWO-SIDED certified tail enclosure")
    print(f"(all from the exact r(n) histogram at R = {Rmax}; lower bounds rounded DOWN, upper bounds rounded UP)")
    print("=" * 118)
    ball = {}
    for name, p, kind in QUANTITIES:
        print(f"\n{name}  (p = {p})")
        print(f"{'R':>4} {'partial (fsum)':>20} {'tail lower':>14} {'tail upper':>14} "
              f"{'certified lower':>16} {'certified upper':>16} {'width':>10} {'width/value':>11}")
        for R in R_LIST:
            h, nmax = select(kind, h2, h3, R, ball=True)
            Pf = sum_float(h, p, nmax)
            Pd = sum_dec(h, p, nmax)
            lo, hi = tail_ball_enclosure(kind, p, R)
            Lo, Hi = Pd + lo - MARGIN, Pd + hi + MARGIN
            ball[(name, R)] = dict(Pf=Pf, Pd=Pd, lo=lo, hi=hi, Lo=Lo, Hi=Hi)
            print(f"{R:>4} {Pf:>20.16g} {dn(lo, 8):>14} {up(hi, 8):>14} {dn(Lo):>16} {up(Hi):>16} "
                  f"{float(Hi - Lo):>10.2e} {float((Hi - Lo) / Hi):>11.2e}")

    # ---------------- consistency checks ----------------
    print()
    print("=" * 118)
    print("CONSISTENCY CHECKS")
    print("=" * 118)
    ok = True
    for name, p, kind in QUANTITIES:
        Us = [cube[(name, R)]["U"] for R in R_LIST]
        Ps = [cube[(name, R)]["Pd"] for R in R_LIST]
        Los = [ball[(name, R)]["Lo"] for R in R_LIST]
        His = [ball[(name, R)]["Hi"] for R in R_LIST]
        c1 = all(Us[i] >= Us[i + 1] for i in range(len(Us) - 1))          # cube upper bounds decrease
        c2 = all(Ps[i] <= Ps[i + 1] for i in range(len(Ps) - 1))          # partial sums increase
        c3 = all(U >= P for U in Us for P in Ps)                           # every U_R >= every P_R'
        c4 = all(Los[i] <= Los[i + 1] and His[i] >= His[i + 1] for i in range(len(Los) - 1))
        c5 = all(Lo <= Hi for Lo in Los for Hi in His)                     # enclosures nested/consistent
        c6 = all(U >= Lo for U in Us for Lo in Los)                        # cube upper >= ball lower
        c7 = all(U >= P for U in Us for P in [ball[(name, R)]["Pd"] for R in R_LIST])
        res = c1 and c2 and c3 and c4 and c5 and c6 and c7
        ok &= res
        print(f"{name:>13}: cube U decreasing {c1}, P increasing {c2}, U>=all P {c3}, "
              f"ball enclosures nested {c4} {c5}, cube U >= ball lower {c6} {c7}  -> {'OK' if res else 'FAIL'}")
    # exact identity Lambda4 = Lambda4_osc + Lambda4_mean on partial sums (decimal, same histogram)
    for R in R_LIST:
        diff = cube[("Lambda4", R)]["Pd"] - cube[("Lambda4_osc", R)]["Pd"] - cube[("Lambda4_mean", R)]["Pd"]
        ok &= abs(diff) < Decimal("1e-40")
    print(f"Lambda4 = Lambda4_osc + Lambda4_mean on every cube partial sum (50-digit): {ok}")
    # known closed form for the 2-D sum: sum'_{Z^2} |k|^-4 = 4 zeta(2) beta(2) = (2 pi^2/3) * Catalan
    catalan = Decimal("0.91596559417721901505460351493238411077414937428167")
    L4m_exact = 2 * PI * PI / 3 * catalan
    Lo, Hi = ball[("Lambda4_mean", Rmax)]["Lo"], ball[("Lambda4_mean", Rmax)]["Hi"]
    inside = Lo <= L4m_exact <= Hi
    ok &= inside
    print(f"Lambda4_mean closed form 4*zeta(2)*beta(2) = {up(L4m_exact, 15)} lies in certified enclosure "
          f"[{dn(Lo, 15)}, {up(Hi, 15)}]: {inside}")
    print(f"ALL CONSISTENCY CHECKS PASSED: {ok}")
    assert ok

    # ---------------- final table ----------------
    print()
    print("=" * 118)
    print(f"FINAL TABLE  (cube partial sums at R = {Rmax}, i.e. {(2 * Rmax + 1) ** 3:,} lattice points in 3-D, "
          f"{(2 * Rmax + 1) ** 2:,} in 2-D)")
    print("certified upper = partial(50-digit) + closed-form tail bound (T3)/(T2) + 1e-30, rounded UP; sqrt rounded UP")
    print("=" * 118)
    print(f"{'quantity':>13} {'p':>4} {'partial sum (fsum)':>20} {'rigorous tail bound':>20} "
          f"{'certified upper bound':>22} {'derived const sqrt':>20} {'tail/partial':>12}")
    final = {}
    for name, p, kind in QUANTITIES:
        d = cube[(name, Rmax)]
        sq = d["U"].sqrt()
        final[name] = (d, sq)
        print(f"{name:>13} {p:>4} {d['Pf']:>20.16g} {up(d['T']):>20} {up(d['U']):>22} {up(sq):>20} "
              f"{100 * float(d['T'] / d['Pd']):>11.3f}%")
    print()
    print(f"{'quantity':>13} {'sharper two-sided certified enclosure (ball, R = ' + str(Rmax) + ')':>60} {'sqrt(upper)':>16}")
    for name, p, kind in QUANTITIES:
        b = ball[(name, Rmax)]
        print(f"{name:>13} {'[' + dn(b['Lo']) + ', ' + up(b['Hi']) + ']':>60} {up(b['Hi'].sqrt()):>16}")
    print()
    print("0.5 % criterion (certified tail bound <= 0.5 % of the cube partial sum):")
    for name, p, kind in QUANTITIES:
        if name in chosen:
            R = chosen[name]
            print(f"  {name:>13}: met at R = {R} ({(2 * R + 1) ** (2 if kind == '2d' else 3):,} points, "
                  f"{cube[(name, R)]['t_hist'] + cube[(name, R)]['t_f'] + cube[(name, R)]['t_d']:.2f} s incl. decimal check)")
        else:
            print(f"  {name:>13}: NOT met for R <= {Rmax} -- the tail decays like R^(3-p) = R^-0.5, the criterion "
                  f"would need R ~ 3e4 (~1e14 points); use the two-sided ball enclosure above instead, whose "
                  f"certified upper bound exceeds the certified lower bound by "
                  f"{100 * float((ball[(name, Rmax)]['Hi'] - ball[(name, Rmax)]['Lo']) / ball[(name, Rmax)]['Hi']):.3f} %.")

    # ---------------- estimates ----------------
    print()
    print("=" * 118)
    print("PLAIN NUMERICAL ESTIMATES OF THE FULL SUMS  -- NOT CERTIFIED, for reference only")
    print("=" * 118)
    print(f"C_4   = int_(max|y_i|>=1) |y|^-4   dy = {C3_4:.12f}   (vs 4 pi = {4 * math.pi:.12f} for the ball exterior)")
    print(f"C_3.5 = int_(max|y_i|>=1) |y|^-3.5 dy = {C3_35:.12f}   (vs 8 pi = {8 * math.pi:.12f})")
    print(f"C2_4  = 1 + pi/2 = {C2_4:.12f};  C2_3.5 = {C2_35:.12f}")
    print(f"{'quantity':>13} {'(E1) cube P_R + C_p L^(3-p)':>28} {'(E2) ball P_R + 4piR^(3-p)/(p-3)':>34} "
          f"{'(E3) enclosure midpoint':>24} {'sqrt(E3)':>14}")
    Lc = Rmax + 0.5
    for name, p, kind in QUANTITIES:
        d = cube[(name, Rmax)]
        b = ball[(name, Rmax)]
        C3 = C3_4 if p == 4.0 else C3_35
        C2 = C2_4 if p == 4.0 else C2_35
        if kind == "3d":
            e1 = d["Pf"] + C3 * Lc ** (3 - p)
            e2 = b["Pf"] + 4 * math.pi * Rmax ** (3 - p) / (p - 3)
        elif kind == "2d":
            e1 = d["Pf"] + C2 * Lc ** (2 - p)
            e2 = b["Pf"] + 2 * math.pi * Rmax ** (2 - p) / (p - 2)
        else:
            e1 = d["Pf"] + C3 * Lc ** (3 - p) - C2 * Lc ** (2 - p)
            e2 = b["Pf"] + 4 * math.pi * Rmax ** (3 - p) / (p - 3) - 2 * math.pi * Rmax ** (2 - p) / (p - 2)
        e3 = float((b["Lo"] + b["Hi"]) / 2)
        print(f"{name:>13} {e1:>28.10f} {e2:>34.10f} {e3:>24.10f} {math.sqrt(e3):>14.10f}")
    print("(E1)-(E3) are estimates with uncontrolled (though small) error; only the certified columns above are rigorous.")

    print()
    print("EXACT TAIL FORMULAS USED (certified columns):")
    print("  3-D cube (Lambda4, Lambda4_osc, Lambda3):  T_R <= 4*pi*[ s0^(3-p)/(p-3) + 2a*s0^(2-p)/(p-2) + a^2*s0^(1-p)/(p-1) ],")
    print("        s0 = R + 1/2 - sqrt(3)/2, a = sqrt(3)/2;  p=4: 4*pi*[1/s0 + a/s0^2 + a^2/(3 s0^3)];")
    print("        p=3.5: 4*pi*[2/sqrt(s0) + (4a/3)/s0^1.5 + (2a^2/5)/s0^2.5].")
    print("  2-D cube (Lambda4_mean):                   T_R <= 2*pi*[ s0^(2-p)/(p-2) + a2*s0^(1-p)/(p-1) ],")
    print("        s0 = R + 1/2 - sqrt(2)/2, a2 = sqrt(2)/2;  p=4: 2*pi*[1/(2 s0^2) + a2/(3 s0^3)].")
    print("  Ball enclosure: same primitives with s0 = R -+ 2a (3-D) / R -+ 2a2 (2-D) and (s +- a)^2 / (s +- a).")
    print(f"\nTotal wall time: {time.time() - t_start:.1f} s")


if __name__ == "__main__":
    main()
