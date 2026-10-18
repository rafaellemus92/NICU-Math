"""Compare results/series.json with the lab-v2 audit's exact series (standard library only).

The audit's line (a) wrote its own exact code, with symbolic nu, and saved the unit-amplitude
series through n = 12 in ../audit_v2/exact/z12_unit.json. Both files store Laurent
coefficients: c[n, m] here is z_{n,m} there (../audit_v2/AUDIT.md section 1), and the
cos(m phi) coefficient is twice that for m >= 1. This script checks that every Z and E
harmonic polynomial agrees exactly (Fraction equality) for n <= 12.

Run from this folder:  python3 compare_audit_v2.py      (< 1 s; prints to stdout; saved output in results/compare_audit_v2.log)
"""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OURS = os.path.join(HERE, "results", "series.json")
THEIRS = os.path.join(HERE, "..", "audit_v2", "exact", "z12_unit.json")


def poly(coeffs):
    """List of rational strings -> list of Fractions, trailing zeros dropped."""
    p = [Fraction(c) for c in coeffs]
    while p and p[-1] == 0:
        p.pop()
    return p


def compare(a, b, nmax):
    """Return (entries compared, list of mismatches) over orders 0..nmax."""
    count, bad = 0, []
    for n in range(nmax + 1):
        an, bn = a.get(str(n), {}), b.get(str(n), {})
        for m in sorted(set(an) | set(bn), key=int):
            pa, pb = poly(an.get(m, [])), poly(bn.get(m, []))
            if not pa and not pb:
                continue
            count += 1
            if pa != pb:
                bad.append((n, int(m)))
    return count, bad


def main():
    ours = json.load(open(OURS))
    theirs = json.load(open(THEIRS))
    nmax = int(theirs["N"])
    print(f"ours:   results/series.json, orders 0..{max(map(int, ours['orders']))}")
    print(f"theirs: ../audit_v2/exact/z12_unit.json, orders 0..{nmax}, amplitudes {theirs['amps']}")
    nz, badz = compare(ours["orders"], theirs["Z"], nmax)
    ne, bade = compare(ours["energy_orders"], theirs["E"], nmax)
    print(f"Z: {nz} harmonic polynomials compared for n <= {nmax}, mismatches: {len(badz)} {badz}")
    print(f"E: {ne} harmonic polynomials compared for n <= {nmax}, mismatches: {len(bade)} {bade}")
    ok = not badz and not bade
    print("agree entry for entry (Fraction equality):", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
