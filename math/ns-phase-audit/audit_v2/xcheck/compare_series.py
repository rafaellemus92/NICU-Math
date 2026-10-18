"""Cross-check: exact symbolic-nu series (exact/z12_unit.json) vs
 (1) float tables (float/tables_float.npz, nu=0,1/28,1/7, two discretisations),
 (2) float complex-nu polynomial coefficients (float/nu_poly.npz),
 (3) package exact jets (results/exact_time_series.json, results/viscosity_identity/node_*.json),
 (4) audit formal-nu jet (code_audit/jet6.json).
Reads only; writes nothing in the package."""
import json, sys
from fractions import Fraction as Fr
import numpy as np

W = ".."
P = "../../periodic_ns_lab_v2"

ex = json.load(open(W + "/exact/z12_unit.json"))
Zx = {int(n): {int(m): [Fr(c) for c in cs] for m, cs in d.items()} for n, d in ex["Z"].items()}
Ex = {int(n): {int(m): [Fr(c) for c in cs] for m, cs in d.items()} for n, d in ex["E"].items()}
NMAX = ex["N"]

def zval(n, m, nu):
    cs = Zx[n].get(m)
    if cs is None:
        return Fr(0)
    return sum(c * nu ** e for e, c in enumerate(cs))

# ---- structural checks on the exact data itself
bad = []
for n in range(NMAX + 1):
    for m, cs in Zx[n].items():
        if Zx[n].get(-m) != cs:
            bad.append(("sym", n, m))
        for e, c in enumerate(cs):
            if c == 0:
                continue
            d = n + 2 - e
            if (d - m) % 2:
                bad.append(("parity d=m", n, m, e))
            if abs(m) >= 2 and d < 3 * abs(m) + 2:
                bad.append(("dmin", n, m, e))
            if abs(m) == 1 and d < 3:
                bad.append(("dmin1", n, m, e))
            if e > n:
                bad.append(("deg", n, m, e))
# energy identity (n+1)E_{n+1} = -2 nu Z_n as polynomials
for n in range(NMAX):
    for m in set(Zx[n]) | set(Ex.get(n + 1, {})):
        lhs = [(n + 1) * c for c in Ex.get(n + 1, {}).get(m, [])]
        rhs = [Fr(0)] + [-2 * c for c in Zx[n].get(m, [])]
        L = max(len(lhs), len(rhs))
        lhs += [Fr(0)] * (L - len(lhs)); rhs += [Fr(0)] * (L - len(rhs))
        if lhs != rhs:
            bad.append(("energy", n, m))
print("exact-data internal checks (sym, parity, d_min, nu-degree, energy identity): violations =", bad)

# ---- (1) float tables
f = np.load(W + "/float/tables_float.npz")
print("\n(1) exact vs float tables  [t^n] Laurent c_{n,m}, all n<=12, all m in DFT range")
for nus, nu in [("0", Fr(0)), ("1/28", Fr(1, 28)), ("1/7", Fr(1, 7))]:
    for tag in "AB":
        c = f[nus + "_c" + tag]; mm = f[nus + "_mm" + tag]
        worst_abs = 0; worst_rel = 0; worst_at = None; worst_rel_at = None
        for n in range(NMAX + 1):
            for i, m in enumerate(mm):
                xv = float(zval(n, int(m), nu))
                fv = c[n, i]
                dabs = abs(fv - xv)
                if dabs > worst_abs:
                    worst_abs, worst_at = dabs, (n, int(m))
                if xv != 0:
                    r = dabs / abs(xv)
                    if r > worst_rel:
                        worst_rel, worst_rel_at = r, (n, int(m), xv)
        print(f"  nu={nus:5s} disc {tag}: max abs diff {worst_abs:.2e} at {worst_at}; "
              f"max rel diff on nonzero exact entries {worst_rel:.2e} at {worst_rel_at}")

# ---- (2) float complex-nu polynomial coefficients
d = np.load(W + "/float/nu_poly.npz"); a, mm = d["a"], d["mm"]
print("\n(2) exact vs float complex-nu DFT coefficients a[n,e,m] (r=1/2: noise ~ 5e-14 * 2^e)")
worst = []
for n in range(NMAX + 1):
    for i, m in enumerate(mm):
        cs = Zx[n].get(int(m), [])
        for e in range(16):
            xv = float(cs[e]) if e < len(cs) else 0.0
            fv = a[n, e, i]
            dabs = abs(fv - xv) * 0.5 ** e  # scaled to the sampling radius
            worst.append((dabs, n, int(m), e, xv, fv.real))
worst.sort(reverse=True)
print("  largest r^e-scaled differences:")
for w in worst[:6]:
    print("   ", "%.2e n=%d m=%d e=%d exact=%.15g float=%.15g" % w)
# relative differences on all nonzero exact entries with |r^e * exact| > 1e-10
rel = []
for dabs, n, m, e, xv, fv in worst:
    if xv != 0 and abs(xv) * 0.5 ** e > 1e-10:
        rel.append((abs(fv - xv) / abs(xv), n, m, e, xv, fv))
rel.sort(reverse=True)
print("  largest relative diffs on exact nonzero entries:")
for w in rel[:5]:
    print("   ", "%.2e n=%d m=%d e=%d exact=%.15g float=%.15g" % w)

# ---- (3) package exact jets (exact rationals, compare EXACTLY)
def pkg_series(fn):
    dd = json.load(open(fn))
    out = {}
    for s in dd["series"]:
        out[s["time_power"]] = {int(m): (Fr(v["real"]), Fr(v["imag"])) for m, v in s["laurent_coefficients"].items()}
    return Fr(dd["nu"]), out

print("\n(3) exact vs package exact jets (Fraction equality)")
files = [P + "/results/exact_time_series.json"] + [P + f"/results/viscosity_identity/node_{i}.json" for i in range(7)]
for fn in files:
    nu, ser = pkg_series(fn)
    mism = []
    for n, dm in ser.items():
        ms = set(dm) | {m for m in Zx[n] if zval(n, m, nu) != 0}
        for m in ms:
            re, im = dm.get(m, (Fr(0), Fr(0)))
            if im != 0 or re != zval(n, m, nu):
                mism.append((n, m, re, zval(n, m, nu)))
    print(f"  {fn.split('/')[-1]:24s} nu={str(nu):5s} orders {min(ser)}..{max(ser)}: mismatches {len(mism)} {mism[:3]}")

# ---- (4) audit jet6 formal-nu polynomials
jt = json.load(open(W + "/code_audit/jet6.json"))
mism = []
for n, dm in jt.items():
    n = int(n)
    for m, es in dm.items():
        m = int(m)
        for e, (re, im) in es.items():
            e = int(e)
            cs = Zx[n].get(m, [])
            xv = cs[e] if e < len(cs) else Fr(0)
            if Fr(re) != xv or Fr(im) != 0:
                mism.append((n, m, e, re, xv))
    # also exact entries missing from audit
    for m, cs in Zx[n].items():
        for e, c in enumerate(cs):
            if c != 0 and str(e) not in jt[str(n)].get(str(m), {}):
                mism.append(("missing", n, m, e))
print("\n(4) exact vs audit formal-nu jet6.json: mismatches", len(mism), mism[:3])

# ---- quoted values in reports
print("\nquoted-value spot checks:")
print("  z62 =", Zx[6][2], " z72 =", Zx[7][2], " z82 =", Zx[8][2])
print("  z60(nu=0) float=", float(Zx[6][0][0]), " (float report 0.040448559076002492)")
print("  z93 =", Zx[9][3], float(Zx[9][3][0]), " (float LD -1.0093283217484565624e-4)")
print("  z10,3 slope", float(Zx[10][3][1]), " (float LD 1.1401604940471467415e-3)")
print("  z12,4 =", float(Zx[12][4][0]), " (float LD -9.345147146365418e-7)")
print("  z71(nu=0) =", float(Zx[7][1][0]))
