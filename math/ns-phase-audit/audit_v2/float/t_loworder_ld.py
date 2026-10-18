"""Low orders n<=5 (and n=6 m=2) in 80-bit long double: exact nu-polynomials of
c_{n,0}, c_{n,1}, check that |m|>=2 vanish for n<=5, and rational
identification of every nu^e coefficient (unit amplitudes).
N=16 (>= 2*6+3), M=17 phases (>= 2*(6+2)+1), complex nu circle L=8, r=1/2
(nu-degree <= n <= 6 < 8)."""
import time, numpy as np
from fractions import Fraction
from decimal import Decimal, getcontext
from nsseries import Grid, param_scan
getcontext().prec = 40
g = Grid(16, dtype=np.clongdouble)
t = time.time()
a, mm = param_scan("nu", 8, 0.5, 17, 6, g)
print("time", time.time() - t)
def A(n, e, m):
    return a[n, e, int(np.where(mm == m)[0][0])]
def frac(x):
    return Fraction(Decimal(np.format_float_scientific(x, precision=25, unique=False)))
noise = max(abs(A(n, e, m)) * 0.5 ** e for n in range(7) for e in range(n + 1, 8) for m in mm)
print("noise floor (e>n, provably zero), times r^e:", float(noise))
big2 = max(abs(A(n, e, m)) for n in range(6) for e in range(8) for m in mm if abs(m) >= 2)
print("max over n<=5, all e, |m|>=2 of |coef|:", float(big2))
thr = 1e-15
for n in range(7):
    for m in ([0, 1] if n < 6 else [0, 1, 2]):
        terms = []
        for e in range(8):
            v = A(n, e, m)
            if abs(v) * 0.5 ** e > thr:
                fr = frac(v.real)
                q = fr.limit_denominator(10 ** 7)
                rel = abs(float((Fraction(q) - fr) / fr))
                terms.append(f"({q}){'' if e == 0 else ' nu' + ('' if e == 1 else '^' + str(e))} [rel {rel:.0e}]")
        print(f"c_{{{n},{m}}} = " + (" + ".join(terms) if terms else "0"))
