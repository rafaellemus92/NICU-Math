"""T5b: Schwartz-Zippel style test of the single-monomial predictions at
random real (signed) amplitude tuples and nu, plus homogeneity
Z_n(lambda A, lambda nu) = lambda^{n+2} Z_n(A, nu)  (i.e. d+e = n+2) for all (n,m).
Predictions (constants from unit-amplitude runs):
  c62  = C62  a^2 b^2 g^2 d^2            C62 = -6487/3110400
  c72  = C72  nu a^2 b^2 g^2 d^2         C72 = 207269/14515200 (identified in long double)
  c93  = C93  a^3 b^2 g^3 d^3
  c10,3= C103 nu a^3 b^2 g^3 d^3
  c12,4= C124 a^4 b^2 g^4 d^4
Note: for a negative delta the Laurent index convention is p = delta e^{i phi}."""
import numpy as np
from nsseries import Grid, phi_scan, laurent
g = Grid(28)
nmax = 12
_, c1, mm, _ = phi_scan(32, nmax, g, nu=1/28)
C = {(6, 2): laurent(c1, mm, 6, 2).real, (7, 2): laurent(c1, mm, 7, 2).real * 28,
     (9, 3): laurent(c1, mm, 9, 3).real, (10, 3): laurent(c1, mm, 10, 3).real * 28,
     (12, 4): laurent(c1, mm, 12, 4).real}
expo = {(6, 2): (2, 2, 2, 2, 0), (7, 2): (2, 2, 2, 2, 1), (9, 3): (3, 2, 3, 3, 0), (10, 3): (3, 2, 3, 3, 1), (12, 4): (4, 2, 4, 4, 0)}
print("constants:", {k: f"{v:+.15e}" for k, v in C.items()})
rng = np.random.default_rng(20261016)
worst = {k: 0.0 for k in C}
for trial in range(6):
    a, b, gm, d = rng.uniform(0.4, 1.6, 4) * rng.choice([-1, 1], 4)
    nu = rng.uniform(-0.2, 0.2)
    _, c, mm, _ = phi_scan(32, nmax, g, alpha=a, beta=b, gamma=gm, delta=d, nu=nu)
    line = []
    for k in C:
        ea, eb, eg, ed, en = expo[k]
        pred = C[k] * a**ea * b**eb * gm**eg * d**ed * nu**en
        got = laurent(c, mm, *k)
        rel = abs(got - pred) / abs(pred)
        worst[k] = max(worst[k], rel)
        line.append(f"c{k}: {got.real:+.6e} pred {pred:+.6e} rel {rel:.1e}")
    print(f"trial {trial}: (a,b,g,d,nu)=({a:+.3f},{b:+.3f},{gm:+.3f},{d:+.3f},{nu:+.4f})\n   " + "\n   ".join(line))
print("worst relative deviation from predicted monomial:", {k: f"{v:.1e}" for k, v in worst.items()})
# homogeneity d+e = n+2 for every (n,m)
base = dict(alpha=0.83, beta=1.17, gamma=1.29, delta=0.71, nu=0.05)
_, c0, mm, _ = phi_scan(32, nmax, g, **base)
for lam in [0.6, -1.3]:
    sc = {k: v * lam for k, v in base.items()}
    _, cl, _, _ = phi_scan(32, nmax, g, **sc)
    worst = 0.0; worst_abs = 0.0; minsig = 1.0
    for n in range(nmax + 1):
        for i, m in enumerate(mm):
            ref = c0[n, i] * lam ** (n + 2)
            dev = abs(cl[n, i] - ref)
            worst_abs = max(worst_abs, dev)
            if abs(ref) > 1e-13:
                worst = max(worst, dev / abs(ref)); minsig = min(minsig, abs(ref))
    print(f"homogeneity lambda={lam}: over all n<=12, all m: max abs dev = {worst_abs:.1e}; max rel dev on entries >1e-13 = {worst:.1e} (smallest such entry {minsig:.1e})")
