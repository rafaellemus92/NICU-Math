"""Cross-check of two independent computations of the b^2 response at T = 0.5 (nu = 1/28, a = c = d = 1):

  * the archive "all-time-phase-response" (Codex, 18 October) integrates the variational equations for
    q1, q2 directly and reports the phi-harmonics of (E2, Z2, S2), the b^2 coefficients of E, Z, S, at
    N = 24, twelve phases (results/atpr_refined.json, copied from its results/refined.json,
    runs[-1].harmonics_E_Z_S);
  * this folder's full_family_dns.py solves the full equations at finite b and the phi-harmonics of
    (O_b - O_0)/b^2 are read from results/long_b.json (b = 1/4 and b = 1, eight phases) with the
    b = 0 baseline from results/reduced_family_t20.json.

Agreement to O(b^2) relative (the b^4 terms) is the expectation: ~1e-3 at b = 1/4, a few percent at b = 1.
Run: python3 crosscheck_variational.py
"""
import json

ref = json.load(open("results/atpr_refined.json"))["runs"][-1]["harmonics_E_Z_S"]
long = json.load(open("results/long_b.json"))
base = {round(r["t"], 3): r for r in json.load(open("results/reduced_family_t20.json"))}
b0 = base[0.5]
print("phi-harmonic m, observable: variational (archive)   finite-b DNS (O_b - O_0)/b^2   ratio")
for bkey in sorted(long, key=float):
    b = float(bkey); b2 = b * b
    row = next(r for r in long[bkey] if abs(r["t"] - 0.5) < 1e-9)
    print(f"b = {b}")
    for m, lab in (("0", "A"), ("1", "B1"), ("2", "B2"), ("3", "B3")):
        for j, name in enumerate(("E", "Z", "S")):
            v = ref[m]["cos"][j]
            mine_b = row[name].get(lab)
            mine_0 = b0[name].get(lab, 0.0) if m in ("0", "1", "2") else 0.0
            if mine_b is None:
                continue
            d = (mine_b - mine_0) / b2
            ratio = d / v if abs(v) > 1e-12 else float("nan")
            print(f"  m={m} {name}: {v:+.6e}   {d:+.6e}   {ratio:.4f}")
