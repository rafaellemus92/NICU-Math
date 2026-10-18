"""T5a: per-amplitude polynomial degree structure of every c_{n,m}.
For each amplitude X in (alpha, beta, gamma, delta): X = e^{2 pi i l/16},
l=0..15 (complex circle), other amplitudes and nu at GENERIC values
(alpha=0.83, beta=1.17, gamma=1.29, delta=0.71, nu=0.05) to avoid accidental
cancellations, phases M=32, N=28, nmax=12.  Amplitude degree of [t^n]Z is
<= n+2 <= 14 < 16 so the DFT is alias-free; degrees k > n+2 are provably zero
and give the noise floor.  Saves amp_degree.npz."""
import os, sys, time, numpy as np
from nsseries import Grid, param_scan
g = Grid(28)
nmax = 12
base = dict(alpha=0.83, beta=1.17, gamma=1.29, delta=0.71, nu=0.05)
out = {}
if os.path.exists("amp_degree.npz") and "--recompute" not in sys.argv:
    d = np.load("amp_degree.npz")
    out = {k: d[k] for k in d.files}
else:
    for name in ["alpha", "beta", "gamma", "delta"]:
        t = time.time()
        a, mm = param_scan(name, 16, 1.0, 32, nmax, g, base=base)
        out[name] = a
        out["mm"] = mm
        print(name, "time", time.time() - t, flush=True)
    np.savez("amp_degree.npz", **out)
mm = out["mm"]
def A(name, n, k, m):
    return out[name][n, k, int(np.where(mm == m)[0][0])]
noise = max(abs(A(nm, n, k, m)) for nm in ["alpha","beta","gamma","delta"] for n in range(nmax+1) for k in range(n+3, 16) for m in mm)
print("noise floor (degrees k > n+2, provably zero):", noise)
thr = 1e-12
names = ["alpha", "beta", "gamma", "delta"]
print("\ndegrees present (|coef| > %.0e) per variable, for m=0..4" % thr)
viol = []
for n in range(nmax + 1):
    for m in range(0, 5):
        degs = {nm: [k for k in range(16) if abs(A(nm, n, k, m)) > thr] for nm in names}
        if any(degs.values()):
            print(f"n={n:2d} m={m}: " + "  ".join(f"{nm[0]}:{degs[nm]}" for nm in names))
for n in range(nmax + 1):
    for m in range(-(n + 2), n + 3):
        for nm in names:
            for k in range(16):
                v = abs(A(nm, n, k, m))
                if v <= thr:
                    continue
                if nm in ("alpha", "gamma", "delta"):
                    if k < abs(m): viol.append((nm, "deg>=|m|", n, m, k, v))
                    if (k - m) % 2: viol.append((nm, "deg=m mod 2", n, m, k, v))
                if nm == "beta":
                    if k % 2: viol.append((nm, "even", n, m, k, v))
                    if abs(m) >= 2 and k < 2: viol.append((nm, "deg>=2 for |m|>=2", n, m, k, v))
print("\nviolations of: deg_{alpha,gamma,delta} >= |m|, = m mod 2; deg_beta even, >=2 if |m|>=2 :", viol if viol else "none")
ex = -6487 / 3110400
b = base
print("\nleading single-monomial checks (coefficient of X^k at generic others):")
for (n, m, pred) in [(6, 2, (2, 2, 2, 2)), (7, 2, (2, 2, 2, 2)), (9, 3, (3, 2, 3, 3)), (10, 3, (3, 2, 3, 3)), (12, 4, (4, 2, 4, 4))]:
    for nm, k in zip(names, pred):
        others = [x for x in range(16) if x != k]
        lead = A(nm, n, k, m)
        rest = max(abs(A(nm, n, x, m)) for x in others)
        print(f" c_{{{n},{m}}}: {nm}^{k} coef = {lead.real:+.12e}  max|other degrees| = {rest:.1e}")
# value consistency: for c_{6,2}: coef of alpha^2 at others = C beta^2 gamma^2 delta^2 with C=c62(unit)
C = ex
print("\n c62: alpha^2 coef / (beta^2 gamma^2 delta^2) =", (A("alpha", 6, 2, 2) / (b['beta']**2*b['gamma']**2*b['delta']**2)).real, " vs -6487/3110400 =", C)
print(" c62: beta^2 coef / (alpha^2 gamma^2 delta^2)  =", (A("beta", 6, 2, 2) / (b['alpha']**2*b['gamma']**2*b['delta']**2)).real)
print(" c62: gamma^2 coef / (alpha^2 beta^2 delta^2)  =", (A("gamma", 6, 2, 2) / (b['alpha']**2*b['beta']**2*b['delta']**2)).real)
print(" c62: delta^2 coef / (alpha^2 beta^2 gamma^2)  =", (A("delta", 6, 2, 2) / (b['alpha']**2*b['beta']**2*b['gamma']**2)).real)
C93 = -1.0093283217484565624e-04
print(" c93: alpha^3 coef / (beta^2 gamma^3 delta^3) =", (A("alpha", 9, 3, 3) / (b['beta']**2*b['gamma']**3*b['delta']**3)).real, " vs unit-amplitude c93 =", C93)
C72 = 207269 / 14515200
print(" c72: alpha^2 coef / (nu beta^2 gamma^2 delta^2) =", (A("alpha", 7, 2, 2) / (b['nu']*b['beta']**2*b['gamma']**2*b['delta']**2)).real, " vs 207269/14515200 =", C72)
