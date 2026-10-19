"""Adversarial checks of the two structural tools of PLAN.md C-E, in exact rationals / 50-digit decimals."""
import random, json, sys
from fractions import Fraction as Fr
from decimal import Decimal as Dd, getcontext
random.seed(20261019)
def majorant(w): return [max(w[i:]) for i in range(len(w))]
def abel(phi, B): return phi[-1] * B[-1] + sum((phi[i] - phi[i + 1]) * B[i] for i in range(len(phi) - 1))
# T1. summation by parts against cumulative upper bounds: implemented form vs three broken forms
ok, broken = 0, {'no majorant': 0, 'no terminal term': 0, 'lower-index boundary (B_{i-1})': 0}
for trial in range(4000):
    n = random.randint(2, 30)
    X = [Fr(random.randint(0, 50), random.randint(1, 9)) for _ in range(n)]
    w = [Fr(random.randint(1, 60), random.randint(1, 7)) for _ in range(n)]
    cum = [sum(X[:i + 1]) for i in range(n)]
    B = [cb + Fr(random.randint(0, 20), random.randint(1, 9)) * random.randint(0, 1) for cb in cum]   # upper bounds, possibly non-monotone
    direct = sum(a * b for a, b in zip(w, X))
    ok += direct <= abel(majorant(w), B)
    broken['no majorant'] += direct > abel(w, B)
    broken['no terminal term'] += direct > abel(majorant(w), B) - majorant(w)[-1] * B[-1]
    phi = majorant(w); Bm = [Fr(0)] + B[:-1]
    broken['lower-index boundary (B_{i-1})'] += direct > phi[-1] * Bm[-1] + sum((phi[i] - phi[i + 1]) * Bm[i] for i in range(n - 1))
print(f'T1 summation by parts: implemented form valid in {ok}/4000 trials; violations of broken forms: {broken}')
# T2. propagation weights on x' = (m(t) - nu) x + f(t), x(0) = 0, exact on fine subcells (rates and sources piecewise constant)
getcontext().prec = 50
nu, n, sub, Dl = Dd(1) / 28, 12, 40, Dd('0.05')
h = Dl / sub; worst_ok, worst_bad = Dd(-1), Dd(-1)
for trial in range(60):
    rates = [[Dd(random.uniform(5, 40)) for _ in range(sub)] for _ in range(n)]        # m on each fine subcell
    srcs = [[Dd(random.uniform(0, 1)) ** 4 * (10 if s < 3 else 1) for s in range(sub)] for _ in range(n)]   # front-loaded sources
    mcell = [max(r) for r in rates]; fcell = [max(s) for s in srcs]                    # cellwise upper bounds
    Cm = [Dd(0)]
    for k in range(n): Cm.append(Cm[-1] + (mcell[k] - nu) * Dl)
    x = Dd(0)
    for j in range(n):
        for s in range(sub):
            a = rates[j][s] - nu; e = (a * h).exp()
            x = e * x + srcs[j][s] * (e - 1) / a
            good = sum(((Cm[j + 1] - Cm[i]).exp() * fcell[i] * Dl for i in range(j + 1)), Dd(0))      # E(i,j): cells i..j inclusive
            bad = sum(((Cm[j + 1] - Cm[i + 1]).exp() * fcell[i] * Dl for i in range(j + 1)), Dd(0))   # source cell excluded
            worst_ok = max(worst_ok, x / good); worst_bad = max(worst_bad, x / bad)
print(f'T2 propagation weights: max exact/bound with inclusive E(i,j) = {float(worst_ok):.4f} (<= 1 required); '
      f'with the source cell excluded = {float(worst_bad):.4f} ({"violates" if worst_bad > 1 else "no violation"})')
# T3. cumulative envelopes used by the summation by parts are nondecreasing (not required, a sanity check)
sv = json.load(open(sys.argv[1]))
print('T3 D_w,j nondecreasing in j:', all(a <= b for a, b in zip(sv['Dw'], sv['Dw'][1:])),
      '; K_j nondecreasing:', all(a <= b for a, b in zip(sv['K'], sv['K'][1:])))
