#!/usr/bin/env python3
"""Exact tests of the orchestrator's structural predictions P1, P2.
usage: test_predictions.py [Nmax_P1] [Nmax_interp]
"""
import sys, time, json
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from nsseries import series, laurent_series, fstr, poly_str

NP1 = int(sys.argv[1]) if len(sys.argv) > 1 else 10
NI = int(sys.argv[2]) if len(sys.argv) > 2 else 9
report = {}


def Zof(amps, N, prune=True):
    U = series(*amps, N, verbose=False, prune=prune)
    return U, laurent_series(U, N, 'curl')


def polyeq(a, b):
    L = max(len(a), len(b))
    a = list(a) + [0] * (L - len(a)); b = list(b) + [0] * (L - len(b))
    return all(Fr(x) == Fr(y) for x, y in zip(a, b))


# ------------------------------------------------------------------ P1
print("=== P1: beta = 0 ===")
P1 = []
for amps in [(1, 0, 1, 1), (2, 0, 5, 7), (Fr(3, 2), 0, Fr(-1, 3), 2)]:
    t0 = time.time()
    U, Z = Zof([Fr(a) for a in amps], NP1)
    harm = {n: sorted(Z[n]) for n in range(NP1 + 1)}
    bad = {n: h for n, h in harm.items() if any(abs(m) >= 2 for m in h)}
    print(f" amps={amps}: Z_n harmonics for n=0..{NP1}: max|m| = {max(max(abs(m) for m in h) for h in harm.values())}; violations: {bad}  ({time.time()-t0:.1f}s)")
    P1.append({"amps": [str(a) for a in amps], "N": NP1, "harmonics": harm, "violations": bad})
# structural check on the FULL (unpruned) velocity series for beta=0
a, g, d = Fr(2), Fr(5), Fr(7)
Nst = 8
U, _ = Zof([a, Fr(0), g, d], Nst, prune=False)
nu_shape_ok = True; kz_ok = True; u3_ok = True; u2_ok = True
fact = 1
for n in range(Nst + 1):
    if n: fact *= n
    for K, v in U[n].items():
        kx, ky, kz, m = K
        if kz != 0: kz_ok = False
        if any(v[1]): u2_ok = False
        if any(v[0]):
            # in-plane: must be alpha e^{-nu t} sin y only
            if K not in ((0, 1, 0, 0), (0, -1, 0, 0)): nu_shape_ok = False
            else:
                expect = [0] * n + [(-a / 2 if ky == 1 else a / 2) * Fr((-1) ** n, fact)]
                if not polyeq(v[0], expect): nu_shape_ok = False
        if any(v[2]) and (kx, m) not in ((1, 0), (-1, 0), (1, 1), (-1, -1)): u3_ok = False
# linearity of u3 in (gamma, delta): doubling gamma, delta doubles u3, leaves u1
U2, _ = Zof([a, Fr(0), 2 * g, 2 * d], Nst, prune=False)
lin_ok = set(U2[Nst]) == set(U[Nst]) and all(
    polyeq(U2[Nst][K][2], [2 * x for x in U[Nst][K][2]]) and polyeq(U2[Nst][K][0], U[Nst][K][0]) for K in U[Nst])
print(f" structure (alpha,gamma,delta)=(2,5,7), U_0..U_{Nst} unpruned: all kz=0: {kz_ok}; u2==0: {u2_ok}; "
      f"u1 = alpha e^(-nu t) sin y exactly: {nu_shape_ok}; u3 only in (kx,m) in {{(1,0),(-1,0),(1,1),(-1,-1)}}: {u3_ok}; "
      f"u3 linear in (gamma,delta): {lin_ok}")
report["P1"] = {"runs": P1, "kz0": kz_ok, "u2zero": u2_ok, "u1_exact": nu_shape_ok, "u3_kx_m": u3_ok, "u3_linear": lin_ok}

# ------------------------------------------------------------------ P2 (a) homogeneity d+e = n+2
print("=== P2(a): grading d + e = n + 2 (scale amplitudes by lam) ===")
Nh = 9
_, Z1 = Zof([Fr(1)] * 4, Nh)
grad_ok = True
for lam in (Fr(2), Fr(-3, 5)):
    _, Zl = Zof([lam] * 4, Nh)
    for n in range(Nh + 1):
        for m in set(Z1[n]) | set(Zl[n]):
            p1 = Z1[n].get(m, []); pl = Zl[n].get(m, [])
            exp_ = [Fr(x) * lam ** (n + 2 - e) for e, x in enumerate(p1)]
            if not polyeq(pl, exp_):
                grad_ok = False; print("  grading violated", n, m)
print(f" grading d+e=n+2 holds for all n<={Nh}, all m, lam in (2,-3/5): {grad_ok}")
report["P2_grading"] = grad_ok

# ------------------------------------------------------------------ P2 (b) monomial at n=6,7 for m=2
print("=== P2(b): amplitude monomial of the m=2 coefficient at n=6,7 (and m=3 at n=9,10) ===")
Nb = 10
_, Zu = Zof([Fr(1)] * 4, Nb)
mono = []
for amps in [(2, 3, 5, 7), (1, 2, 1, 3), (Fr(1, 2), Fr(-2, 3), Fr(3, 4), Fr(5, 7))]:
    A = [Fr(x) for x in amps]
    _, Za = Zof(A, Nb)
    for (n, m) in [(6, 2), (7, 2), (8, 2), (9, 3), (10, 3)]:
        mon = A[0] ** m * A[1] ** 2 * A[2] ** m * A[3] ** m
        pa = Za[n].get(m, []); pu = Zu[n].get(m, [])
        ok = polyeq(pa, [mon * Fr(x) for x in pu])
        print(f" amps={amps} n={n} m={m}: z = {poly_str(pa)} ; unit*a^{m}b^2g^{m}d^{m} = {poly_str([mon*Fr(x) for x in pu])} ; equal: {ok}")
        mono.append({"amps": [str(x) for x in amps], "n": n, "m": m, "z": [fstr(x) for x in pa],
                     "monomial": fstr(mon), "equal": ok})
report["P2_monomial"] = mono

# ------------------------------------------------------------------ P2 (c) univariate structure in each amplitude
print(f"=== P2(c): exact univariate polynomial structure of z_(n,m) in each amplitude, n<={NI} ===")
base = [Fr(2, 3), Fr(5, 7), Fr(11, 13), Fr(17, 19)]   # generic values for the other amplitudes
D = NI + 2   # total amplitude degree of Z_n is <= n+2
pts = [Fr(i + 1, 1) for i in range(D + 1)]


def interp(xs, ys):
    """exact Lagrange -> coefficient list"""
    n = len(xs); coef = [Fr(0)] * n
    for i in range(n):
        num = [Fr(1)]; den = Fr(1)
        for j in range(n):
            if j == i: continue
            num = [Fr(0)] + num
            for k in range(len(num) - 1):
                num[k] -= xs[j] * num[k + 1]
            den *= xs[i] - xs[j]
        for k in range(n):
            coef[k] += ys[i] * num[k] / den
    return coef


names = ["alpha", "beta", "gamma", "delta"]
struct = {}
viol = []
for ia in range(4):
    t0 = time.time()
    samples = []
    for s in pts:
        A = list(base); A[ia] = s
        samples.append(Zof(A, NI)[1])
    for n in range(NI + 1):
        ms = set().union(*[set(Zs[n]) for Zs in samples])
        for m in ms:
            if m < 0: continue
            for e in range(n + 1):
                ys = []
                for Zs in samples:
                    p = Zs[n].get(m, [])
                    ys.append(Fr(p[e]) if e < len(p) else Fr(0))
                if not any(ys): continue
                c = interp(pts, ys)
                degs = [k for k, x in enumerate(c) if x]
                struct.setdefault(f"n={n},m={m},e={e}", {})[names[ia]] = degs
                mn = min(degs); par = {k % 2 for k in degs}
                if ia in (0, 2, 3):
                    if mn < m or par != {m % 2}: viol.append((n, m, e, names[ia], degs))
                else:
                    if par != {0} or (m >= 2 and mn < 2): viol.append((n, m, e, names[ia], degs))
    print(f"  {names[ia]} done ({time.time()-t0:.1f}s)", flush=True)
for key in sorted(struct, key=lambda s: [int(x.split('=')[1]) for x in s.split(',')]):
    print(f"  {key}: degrees present " + "; ".join(f"{a}:{struct[key].get(a)}" for a in names))
print(f" P2 counting violations (min degree / parity rules): {viol}")
report["P2_univariate"] = {"struct": struct, "violations": [list(map(str, v)) for v in viol]}
json.dump(report, open(__file__.rsplit('/', 1)[0] + "/predictions_report.json", "w"), indent=1, default=str)
