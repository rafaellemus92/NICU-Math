#!/usr/bin/env python3
"""Format the exact Laurent tables from a run_series.py JSON.
usage: tables.py series.json [nmax]"""
import sys, json
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from nsseries import poly_str, fstr

r = json.load(open(sys.argv[1]))
nmax = int(sys.argv[2]) if len(sys.argv) > 2 else r["N"]
nu28 = Fr(1, 28)
print(f"amps={r['amps']}  (Laurent coefficient z_(n,m) of e^(i m phi) in [t^n]Z; z_(n,-m) = z_(n,m), all real)")
for n in range(nmax + 1):
    h = r["Z"][str(n)]
    ms = sorted(int(m) for m in h)
    print(f"n={n}: harmonics m in {ms}")
    for m in ms:
        if m < 0: continue
        p = [Fr(x) for x in h[str(m)]]
        v = sum(Fr(x) * nu28 ** e for e, x in enumerate(p))
        cosf = "" if m == 0 else f"   [cos({m}phi) coeff = 2*z = {poly_str([2*Fr(x) for x in p])}]"
        print(f"   z_({n},{m:+d}) = {poly_str(p)}{cosf}   @nu=1/28: {fstr(v)} = {float(v):.15g}")
