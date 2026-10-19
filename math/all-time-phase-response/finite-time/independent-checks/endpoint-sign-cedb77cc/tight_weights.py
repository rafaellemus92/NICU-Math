"""Tight-case test of the propagation weights of PLAN.md C (and the same structure in D, E): x' = (m - nu) x + f, x(0) = 0,
with m and f constant on each cell, so the exact solution is known in closed form. The inclusive weight
exp(sum_{k=i..j}(m_k - nu) Delta) must dominate at every t <= t_{j+1}; the weight that excludes the source cell must fail.
50-digit decimals, fixed seed. Usage: python3 -I -B tight_weights.py"""
import random
from decimal import Decimal as Dd, getcontext
getcontext().prec = 50; random.seed(7)
nu, n, Dl = Dd(1) / 28, 12, Dd('0.05')
worst_ok, worst_bad = Dd(-1), Dd(-1)
for trial in range(200):
    m = [Dd(random.uniform(2.5, 40)) for _ in range(n)]; f = [Dd(random.uniform(0, 1)) for _ in range(n)]
    Cm = [Dd(0)]
    for k in range(n): Cm.append(Cm[-1] + (m[k] - nu) * Dl)
    x = Dd(0)
    for j in range(n):
        for frac in (Dd('0.25'), Dd('0.5'), Dd(1)):            # interior times and the right endpoint of cell j
            a = m[j] - nu; e = (a * Dl * frac).exp()
            xt = e * x + f[j] * (e - 1) / a
            good = sum(((Cm[j + 1] - Cm[i]).exp() * f[i] * Dl for i in range(j + 1)), Dd(0))
            bad = sum(((Cm[j + 1] - Cm[i + 1]).exp() * f[i] * Dl for i in range(j + 1)), Dd(0))
            worst_ok = max(worst_ok, xt / good); worst_bad = max(worst_bad, xt / bad)
        a = m[j] - nu; e = (a * Dl).exp(); x = e * x + f[j] * (e - 1) / a
print(f'tight case: max exact/bound, inclusive E(i,j) = {float(worst_ok):.4f} (<= 1 required); '
      f'source cell excluded = {float(worst_bad):.4f} -> {"VIOLATES" if worst_bad > 1 else "ok"}')
assert worst_ok <= 1 < worst_bad
