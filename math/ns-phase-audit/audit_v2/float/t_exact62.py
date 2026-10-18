"""T1: c_{6,2} vs -6487/3110400 in double (N=16..32 grids, two phase grids) and
in 80-bit long double; also a long-double look at c_{9,3}, c_{12,4},
c_{7,2}/nu, c_{10,3}/nu with continued-fraction rational candidates."""
import time, numpy as np
from fractions import Fraction
from nsseries import Grid, phi_scan, laurent
exact = Fraction(-6487, 3110400)
ex = -6487 / 3110400
print("exact -6487/3110400 =", repr(ex))
for N, M, phi0, nmax in [(16, 17, 0.0, 6), (24, 24, 0.3, 6), (28, 32, 0.0, 12), (32, 36, 0.1234, 12)]:
    for nu in [0.0, 1/28, 1/7]:
        g = Grid(N)
        Z, c, mm, _ = phi_scan(M, nmax, g, nu=nu, phi0=phi0)
        v = laurent(c, mm, 6, 2)
        print(f"double N={N} M={M} phi0={phi0} nu={nu:.5f}: c62={v.real:+.17e} rel.err={(v.real-ex)/abs(ex):+.2e}  Im={v.imag:+.1e}  cos2phi coeff=2*c62={2*v.real:+.15e}")
# long double
ld = np.longdouble
exL = ld(-6487) / ld(3110400)
t = time.time()
g = Grid(16, dtype=np.clongdouble)
for nu in [ld(0), ld(1) / 28, ld(1) / 7]:
    Z, c, mm, _ = phi_scan(17, 6, g, nu=nu)
    v = laurent(c, mm, 6, 2)
    print(f"longdouble N=16 M=17 nu={float(nu):.5f}: c62={np.format_float_scientific(v.real, precision=20)}  rel.err={float((v.real-exL)/abs(exL)):+.2e}  Im={float(v.imag):+.1e}")
print("time", time.time() - t)
# long double, nmax=12 (N=28, M=29) for higher harmonics and rational guesses
t = time.time()
g = Grid(28, dtype=np.clongdouble)
out = {}
for nu in [ld(0), ld(1) / 28]:
    Z, c, mm, _ = phi_scan(29, 12, g, nu=nu)
    out[float(nu)] = (c, mm)
print("time", time.time() - t)
def ratguess(x, maxden):
    f = Fraction(float(x)).limit_denominator(maxden)
    # refine using long double: use string of high precision
    return f
from decimal import Decimal, getcontext
getcontext().prec = 30
def frac_ld(x):
    # exact rational value of a long double
    s = np.format_float_scientific(x, precision=25, unique=False)
    return Fraction(Decimal(s))
c0, mm = out[0.0]
c1, _ = out[1/28]
items = {"c62": laurent(c0, mm, 6, 2).real, "c93": laurent(c0, mm, 9, 3).real, "c12_4": laurent(c0, mm, 12, 4).real,
         "c72/nu": laurent(c1, mm, 7, 2).real * 28, "c10_3/nu": laurent(c1, mm, 10, 3).real * 28,
         "c72(nu=0)": laurent(c0, mm, 7, 2).real, "c10_3(nu=0)": laurent(c0, mm, 10, 3).real,
         "c83(nu=0)": laurent(c0, mm, 8, 3).real, "c11_4(nu=0)": laurent(c0, mm, 11, 4).real, "c52(nu=0)": laurent(c0, mm, 5, 2).real}
for k, v in items.items():
    fr = frac_ld(v)
    cands = []
    for md in [10**6, 10**8, 10**10, 10**12]:
        f = fr.limit_denominator(md)
        cands.append((f, float(abs(Fraction(f) - fr) / abs(fr)) if fr != 0 else 0))
    print(f"{k:12s} = {np.format_float_scientific(v, precision=20)}   candidates:", "; ".join(f"{f} (rel {e:.1e})" for f, e in cands))
